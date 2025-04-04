from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

SKIP_TEXT_KEYWORDS = [
    "skip", "bypass", "omitir", "ir al contenido", 
    "saltar al contenido", "omitir menú", "omitir menu"
]
SKIP_HREF_TARGETS = [
    "#main", "#content", "#principal", "#maincontent", "#contenido"
]

def get_html_lines(html_content):
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    return "\n".join(f"{i+1}: {snippet[i - start]}" for i in range(start, end))

def get_element_info(element, html_lines=None):
    tag = element.name
    text = element.get_text(strip=True)
    evidence = str(element)[:300]
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    snippet = ""
    if line_number != "N/A" and html_lines:
        try:
            snippet = get_line_snippet(html_lines, int(line_number))
        except Exception:
            pass

    return {
        "tag": tag,
        "text": text,
        "evidence": evidence,
        "line_number": line_number,
        "fragment_html": snippet
    }

def format_incidence(inc):
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Check if there's a mechanism (skip link, main landmark, etc.) "
            "to bypass repeated blocks.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n{snippet}"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": element_info.get("evidence", "")
    }

def run_all___2_4_1(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    has_main_landmark = bool(soup.find("main")) or bool(soup.find(attrs={"role": "main"}))

    skip_link_found = False
    for link in soup.find_all("a"):
        href = link.get("href", "").lower()
        text = link.get_text(strip=True).lower()

        if href.startswith("#") and any(skipt in href for skipt in ["main", "content", "principal"]):
            skip_link_found = True
            break
        if any(kw in text for kw in SKIP_TEXT_KEYWORDS):
            skip_link_found = True
            break
        if href in SKIP_HREF_TARGETS:
            skip_link_found = True
            break

    if not has_main_landmark and not skip_link_found:
        # Se refiere a todo el documento, pero generamos una línea neutral con fragmento
        info = {
            "tag": "html",
            "text": "",
            "evidence": "No skip link or main landmark found.",
            "line_number": "N/A",
            "fragment_html": "No <main> tag or skip link (<a href=\"#main\">) detected."
        }

        raw_incidences.append({
            "title": "No mechanism to bypass repeated blocks",
            "type": "Navigation Aid",
            "severity": "High",
            "expected_result": "Provide a skip link or main landmark to quickly bypass repetitive content.",
            "actual_result": "Page lacks skip links or 'main' area to jump to.",
            "remediation": (
                "Add a <main> or role=\"main\", or include a skip link like "
                "<a href=\"#main-content\">Skip to main content</a>."
            ),
            "wcag_reference": "2.4.1",
            "impact": (
                "Keyboard or screen reader users must navigate through repeated content on every page."
            ),
            "page_url": page_url,
            "element_info": info
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
            "Failed checkpoint": "2.4.1",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
