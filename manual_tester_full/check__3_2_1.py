import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

CHANGE_CONTEXT_PATTERNS = [
    r"window\.open",
    r"location\.href",
    r"\.submit\s*\(",
    r"top\.location",
    r"self\.location",
    r"document\.location",
]

def get_html_lines(html_content):
    """Divide el HTML en lista de líneas para extraer contexto."""
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """Devuelve un fragmento con 2 líneas antes/después de line_number, numeradas."""
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    return "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))

def get_element_info(element, html_lines=None):
    """
    Extrae metadatos (tag, snippet, etc.) y un fragmento de HTML
    alrededor de line_number si está presente.
    """
    tag = element.name
    attrs = dict(element.attrs)
    snippet_html = str(element)[:300]
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    fragment_html = ""
    if line_number != "N/A" and html_lines:
        try:
            fragment_html = get_line_snippet(html_lines, int(line_number), context=2)
        except Exception:
            pass

    return {
        "tag": tag,
        "attrs": attrs,
        "snippet": snippet_html,
        "line_number": line_number,
        "fragment_html": fragment_html
    }

def format_incidence(inc):
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the element with 'onfocus'.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n"
            f"{snippet}"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": element_info.get("snippet", "")
    }

def run_all___3_2_1(html_content, page_url, excel="issue_report.xlsx"):
    """
    1. Busca elementos con 'onfocus'.
    2. Verifica si el contenido de 'onfocus' coincide con alguno de los
       patrones que puedan iniciar un cambio de contexto.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    all_tags = soup.find_all(lambda t: t.has_attr("onfocus"))
    for elem in all_tags:
        onfocus_value = elem.get("onfocus", "")
        lower_onfocus = onfocus_value.lower()
        matched = any(re.search(pattern, lower_onfocus) for pattern in CHANGE_CONTEXT_PATTERNS)
        if matched:
            raw_incidences.append({
                "title": "Element triggers context change on focus",
                "type": "On Focus Behavior",
                "severity": "High",
                "expected_result": (
                    "Focusing a component must not automatically change context "
                    "without user activation."
                ),
                "actual_result": f"onfocus contains code that likely changes context: {onfocus_value}",
                "remediation": (
                    "Remove or modify the onfocus script so context doesn't change "
                    "until user explicitly activates it (e.g., on click)."
                ),
                "wcag_reference": "3.2.1",
                "impact": (
                    "Keyboard or screen reader users might unexpectedly lose context "
                    "or get redirected while tabbing."
                ),
                "page_url": page_url,
                "element_info": get_element_info(elem, html_lines=lines)
            })

    formatted = [format_incidence(i) for i in raw_incidences]
    if not formatted:
        formatted.append({
            "Title": "Justificación de los CPs asignados que no generen issues",
            "Steps": "N/A",
            "Bug Type": "N/A",
            "Priority": "N/A",
            "Expected Result": "N/A",
            "Actual Result": "N/A",
            "Suggested resolution(s)": "N/A",
            "Failed checkpoint": "3.2.1",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
