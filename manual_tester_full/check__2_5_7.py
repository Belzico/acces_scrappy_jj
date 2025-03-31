from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

DRAG_ATTRIBUTES = [
    "draggable", "ondrag", "ondragstart", "ondragend", "ondrop"
]

def get_element_info(element):
    return {
        "tag": element.name,
        "attrs": dict(element.attrs),
        "snippet": str(element)[:300]
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Verify if there's an alternative to the drag-and-drop functionality "
            "that can be done via simple pointer actions (click/tap, etc.)."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("snippet", "")
    }

def run_all___2_5_7(html_content, page_url, excel="issue_report.xlsx"):
    """
    Heurística para descubrir posibles componentes que requieran arrastrar (drag&drop)
    y no incluyan un método alternativo de un solo puntero.
    - Busca atributos "draggable", "ondragstart", "ondrop", etc.
    - Reporta la necesidad de verificar si existe una alternativa sin arrastrar.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Buscar cualquier elemento con atributos que sugieran drag & drop
    all_elements = soup.find_all(True)  # Encuentra todos los tags

    for elem in all_elements:
        # Revisamos si alguno de los DRAG_ATTRIBUTES está presente en el elemento
        for drag_attr in DRAG_ATTRIBUTES:
            if drag_attr in elem.attrs:
                # A veces draggable="false" no es un problema
                if drag_attr == "draggable" and elem.attrs[drag_attr] == "false":
                    continue

                # Hemos detectado un componente que potencialmente requiere drag
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
                    "element_info": get_element_info(elem)
                })
                # Rompemos, no queremos reportar el mismo elemento varias veces
                break

    formatted = [format_incidence(i) for i in raw_incidences]

    # Si no hallamos elementos con arrastrar -> sin incidencias
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
