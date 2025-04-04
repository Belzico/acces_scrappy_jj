import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

DRAG_ATTRIBUTES = [
    "draggable", "ondrag", "ondragstart", "ondragend", "ondrop"
]

def get_html_lines(html_content):
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(f"{i+1}: {snippet[i - start]}" for i in range(start, end))
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Devuelve metadatos básicos del elemento (tag, snippet, etc.) y
    un fragmento de HTML alrededor de line_number si está disponible.
    """
    tag = element.name
    text = element.get_text(strip=True)[:80]
    evidence = str(element)[:300]
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"
    
    fragment_html = ""
    if line_number != "N/A" and html_lines:
        try:
            fragment_html = get_line_snippet(html_lines, int(line_number), context=2)
        except ValueError:
            pass

    return {
        "tag": tag,
        "text": text,
        "evidence": evidence,
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
            "2. Verify if there's an alternative to the drag-and-drop functionality "
            "that can be done via simple pointer actions (click/tap, etc.).\n\n"
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
        "Evidence [SS or Video]": element_info.get("evidence", "")
    }

def run_all___2_5_7(html_content, page_url, excel="issue_report.xlsx"):
    """
    Heurística para descubrir posibles componentes que requieran arrastrar (drag&drop)
    y no incluyan un método alternativo de un solo puntero.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    all_elements = soup.find_all(True)
    for elem in all_elements:
        for drag_attr in DRAG_ATTRIBUTES:
            if drag_attr in elem.attrs:
                # draggable="false" no es un problema
                if drag_attr == "draggable" and elem.attrs[drag_attr] == "false":
                    continue

                raw_incidences.append({
                    "title": "Potential drag-and-drop without single-pointer alternative",
                    "type": "Dragging Movements",
                    "severity": "Medium",
                    "expected_result": (
                        "Where drag is used, an alternative method should exist "
                        "for users who cannot perform precise dragging."
                    ),
                    "actual_result": (
                        f"Element '{elem.name}' has attribute '{drag_attr}={elem.attrs[drag_attr]}' "
                        "suggesting drag-based interaction."
                    ),
                    "remediation": (
                        "Provide a single-pointer alternative (e.g. clickable controls, text input) "
                        "so users can operate the same functionality without dragging."
                    ),
                    "wcag_reference": "2.5.7",
                    "impact": (
                        "People with limited mobility or alternative input devices "
                        "may find dragging too difficult or impossible."
                    ),
                    "page_url": page_url,
                    "element_info": get_element_info(elem, html_lines=lines)
                })
                # Rompe para no reportar el mismo elemento varias veces
                break

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
            "Failed checkpoint": "2.5.7",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
