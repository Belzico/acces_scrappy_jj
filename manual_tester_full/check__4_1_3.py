import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

POSSIBLE_STATUS_KEYWORDS = [
    "error", "invalid", "fail", "failed", "warning",
    "success", "successfully", "results returned", "added to", "items in cart",
    "loading", "please wait", "no results", "busy", "completed", "submitted"
]

VALID_STATUS_ROLES = {
    "status", "alert", "log", "progressbar"
}
VALID_LIVE_VALUES = {
    "polite", "assertive"
}

def get_html_lines(html_content):
    """
    Convierte el HTML en una lista de líneas,
    para luego extraer fragmentos alrededor de line_number.
    """
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    lines: lista de líneas del HTML.
    line_number: número de línea (base 1) donde se encontró el elemento.
    context: cuántas líneas antes y después se extraen.

    Retorna un string con el fragmento de HTML alrededor de esa línea.
    """
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(
        f"{i+1}: {lines[i]}"
        for i in range(start, end)
    )
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Extrae metadatos del elemento para evidencia, incluyendo un snippet (fragment_html)
    de 2 líneas antes y 2 después del line_number si está disponible.
    """
    tag = element.name
    text_excerpt = element.get_text(strip=True)[:120]
    evidence = str(element)[:300]
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    snippet_str = ""
    if line_number != "N/A" and html_lines:
        try:
            snippet_str = get_line_snippet(html_lines, int(line_number), context=2)
        except ValueError:
            pass

    return {
        "tag": tag,
        "text": text_excerpt,
        "evidence": evidence,
        "line_number": line_number,
        "fragment_html": snippet_str
    }

def format_incidence(inc):
    elem_info = inc.get("element_info", {})
    snippet = elem_info.get("fragment_html", "")
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Inspect the text that appears to be a status message.\n\n"
            f"HTML snippet (around line {elem_info.get('line_number', 'N/A')}):\n"
            f"{snippet}"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": elem_info.get("evidence", "")
    }

def is_status_role(element):
    """
    Revisa si el elemento o alguno de sus padres tiene un rol/status ARIA
    como role="status", role="alert", o aria-live="polite"/"assertive".
    """
    role_attr = element.get("role", "")
    aria_live = element.get("aria-live", "")

    if role_attr in VALID_STATUS_ROLES:
        return True
    if aria_live in VALID_LIVE_VALUES:
        return True

    parent = element.parent
    while parent and parent.name.lower() != "body":
        parent_role = parent.get("role", "")
        parent_live = parent.get("aria-live", "")
        if parent_role in VALID_STATUS_ROLES or parent_live in VALID_LIVE_VALUES:
            return True
        parent = parent.parent

    return False

def run_all___4_1_3(html_content, page_url, excel="issue_report.xlsx"):
    """
    Busca fragmentos de texto (p, div, span, etc.) con palabras clave de mensajes de estado.
    Verifica si el elemento (o ancestro) está marcado con role="status", aria-live, etc.
    Si no se encuentra => Incidencia.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    possible_text_blocks = soup.find_all(["p", "div", "span", "li", "section"])

    for elem in possible_text_blocks:
        text_lower = elem.get_text(strip=True).lower()

        # Verificar si hay keywords
        if any(kw in text_lower for kw in POSSIBLE_STATUS_KEYWORDS):
            # Chequear si ya está marcado o ancestro con rol
            if not is_status_role(elem):
                raw_incidences.append({
                    "title": "Status message is not marked up for assistive technologies",
                    "type": "Status Message",
                    "severity": "Medium",
                    "expected_result": (
                        "Status messages should have ARIA role or live region "
                        "so screen readers can announce them automatically."
                    ),
                    "actual_result": f"Found text: \"{elem.get_text(strip=True)}\" with no ARIA role or aria-live parent.",
                    "remediation": (
                        "Use role=\"status\" or aria-live=\"polite\"/\"assertive\" to ensure it is announced "
                        "without taking focus."
                    ),
                    "wcag_reference": "4.1.3",
                    "impact": (
                        "Screen reader users won't know an important status has changed without focusing the element."
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
            "Failed checkpoint": "4.1.3",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
