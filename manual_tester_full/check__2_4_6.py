from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

# Palabras vacías o demasiado genéricas
GENERIC_TERMS = {
    "heading", "title", "untitled", "label", "header", "section", "example heading",
    "my heading", "test heading", "my label", "test label", "form label"
}

def get_element_info(element):
    """
    Devuelve información básica del elemento para incluir en el reporte.
    """
    return {
        "tag": element.name,
        "text": element.get_text(strip=True),
        "evidence": str(element)[:300]
    }

def format_incidence(inc):
    """
    Formatea la incidencia para poder exportarla a Excel.
    """
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the element <{inc.get('element_info', {}).get('tag')}> "
            f"with text: \"{inc.get('element_info', {}).get('text')}\"."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "")
    }

def run_all___2_4_6(html_content, page_url, excel="issue_report.xlsx"):
    """
    Verifica encabezados (<h1> ... <h6>) y <label>:
    - Si están vacíos o usan texto genérico => Se reportan como no descriptivos.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 1) Procesar heading tags <h1> ... <h6>
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    for heading in headings:
        text = heading.get_text(strip=True).lower()

        # Heurística: si no hay texto o es genérico, lo marcamos como error
        if not text or text in GENERIC_TERMS:
            raw_incidences.append({
                "title": "Non-descriptive heading",
                "type": "Headings & Labels",
                "severity": "Medium",
                "expected_result": "Headings should clearly describe the content that follows.",
                "actual_result": (
                    f"Heading is empty or uses generic text: \"{text}\""
                ),
                "remediation": (
                    "Replace with a concise, meaningful heading (e.g., "
                    "'About Our Services', 'Instructions', etc.)."
                ),
                "wcag_reference": "2.4.6",
                "impact": (
                    "Users with cognitive or visual disabilities may struggle "
                    "to understand the page structure or content organization."
                ),
                "page_url": page_url,
                "element_info": get_element_info(heading)
            })

    # 2) Procesar <label> de formularios
    labels = soup.find_all("label")
    for lbl in labels:
        text = lbl.get_text(strip=True).lower()
        if not text or text in GENERIC_TERMS:
            raw_incidences.append({
                "title": "Non-descriptive label",
                "type": "Headings & Labels",
                "severity": "Medium",
                "expected_result": (
                    "Labels should clearly indicate what input is requested."
                ),
                "actual_result": f"Label is empty or uses generic text: \"{text}\"",
                "remediation": (
                    "Use descriptive text (e.g., 'First Name', 'Search Terms'). "
                    "If the label must be visually hidden, ensure the accessible name "
                    "is still descriptive."
                ),
                "wcag_reference": "2.4.6",
                "impact": (
                    "People using screen readers or with cognitive impairments may not "
                    "know what the field is for."
                ),
                "page_url": page_url,
                "element_info": get_element_info(lbl)
            })

    # 3) Generar la salida
    formatted = [format_incidence(i) for i in raw_incidences]

    # Si no hubo incidencias, añadimos la justificación final
    if not formatted:
        formatted.append({
            "Title": "Justificación de los CPs asignados que no generen issues",
            "Steps": "N/A",
            "Bug Type": "N/A",
            "Priority": "N/A",
            "Expected Result": "N/A",
            "Actual Result": "N/A",
            "Suggested resolution(s)": "N/A",
            "Failed checkpoint": "2.4.6",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
