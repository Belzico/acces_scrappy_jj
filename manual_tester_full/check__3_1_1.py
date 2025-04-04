from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  # Asegúrate de tener este módulo
import re

def get_html_lines(html_content):
    """Divide el HTML en lista de líneas para extraer snippets de contexto."""
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """Devuelve un fragmento alrededor de line_number (2 líneas antes/después) con numeración."""
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    return "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))

def get_element_info(element, html_lines=None):
    """
    Devuelve información detallada del elemento (tag, snippet) y un fragmento de 
    HTML alrededor de la línea donde se encuentra, si hay line_number disponible.
    """
    tag = element.name if element else "N/A"
    snippet_html = str(element)[:300] if element else ""
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    fragment_html = ""
    if line_number != "N/A" and html_lines:
        try:
            fragment_html = get_line_snippet(html_lines, int(line_number), context=2)
        except Exception:
            pass

    # attrs como dict, si deseas retenerlos
    attrs = dict(element.attrs) if element else {}

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
            "2. Verify that the <html> element contains a valid 'lang' attribute "
            "indicating the primary language of the page (e.g., <html lang=\"en\">).\n\n"
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

def run_all___3_1_1(html_content, page_url, excel="issue_report.xlsx"):
    """
    WCAG 3.1.1 - Language of Page:
    Verifica que el atributo 'lang' esté presente y correctamente definido en <html>.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    html_lines = get_html_lines(html_content)
    raw_incidences = []

    html_tag = soup.find("html")

    if html_tag:
        lang_value = html_tag.get("lang", None)
        if not lang_value or not isinstance(lang_value, str) or len(lang_value.strip()) < 2:
            raw_incidences.append({
                "title": "Missing or invalid 'lang' attribute on <html> element",
                "type": "Language Detection",
                "severity": "High",
                "expected_result": "The <html> element must have a valid 'lang' attribute indicating the primary language of the page.",
                "actual_result": "No 'lang' attribute found or invalid value set in the <html> tag.",
                "remediation": "Add or correct the 'lang' attribute in <html> (e.g., <html lang=\"en\"> or <html lang=\"es\">).",
                "wcag_reference": "3.1.1",
                "impact": (
                    "Assistive technologies may not interpret content correctly, "
                    "impacting comprehension for screen reader users."
                ),
                "page_url": page_url,
                "element_info": get_element_info(html_tag, html_lines)
            })
    else:
        raw_incidences.append({
            "title": "Missing <html> element",
            "type": "Language Detection",
            "severity": "High",
            "expected_result": "The document should have a <html> root element with a 'lang' attribute.",
            "actual_result": "No <html> element found in the document.",
            "remediation": "Ensure the page starts with a valid <html> element and includes a 'lang' attribute.",
            "wcag_reference": "3.1.1",
            "impact": (
                "The language of the page cannot be determined, which may confuse assistive technologies."
            ),
            "page_url": page_url,
            "element_info": {}  # No <html> => no snippet
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
            "Failed checkpoint": "3.1.1",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
