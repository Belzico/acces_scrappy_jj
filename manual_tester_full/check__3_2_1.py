import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

# Heurística: buscar cadenas que posiblemente causen un cambio de contexto:
# "window.open", "location.href", "this.form.submit", "form.submit", etc.
CHANGE_CONTEXT_PATTERNS = [
    r"window\.open",
    r"location\.href",
    r"\.submit\s*\(",
    r"top\.location",
    r"self\.location",
    r"document\.location",
    # Se pueden añadir más (por ejemplo, "focus()", si cambiara el foco a otro lado).
]

def get_element_info(element):
    """Extrae metadatos del elemento para el reporte."""
    return {
        "tag": element.name,
        "attrs": dict(element.attrs),
        "snippet": str(element)[:300]
    }

def format_incidence(inc):
    """Formatea la incidencia en el dict final para exportar a Excel."""
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the element with 'onfocus'."
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

def run_all___3_2_1(html_content, page_url, excel="issue_report.xlsx"):
    """
    1. Parsea el HTML.
    2. Busca elementos con 'onfocus'.
    3. Revisa si el contenido de 'onfocus' coincide con alguno de los patrones
       que pueden iniciar un cambio de contexto (abrir ventana, redirigir, etc.).
    4. Si sí => reporta posible incumplimiento de 3.2.1.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Buscar cualquier elemento con onfocus
    all_tags = soup.find_all(lambda t: t.has_attr("onfocus"))

    for elem in all_tags:
        onfocus_value = elem.get("onfocus", "")
        lower_onfocus = onfocus_value.lower()

        # Comprobamos si coincide con alguno de CHANGE_CONTEXT_PATTERNS
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
                    "Remove or modify the onfocus script so that the context does not change "
                    "until user explicitly activates the element (e.g., on click)."
                ),
                "wcag_reference": "3.2.1",
                "impact": (
                    "Keyboard or screen reader users might unexpectedly lose context or get redirected "
                    "as they tab into controls."
                ),
                "page_url": page_url,
                "element_info": get_element_info(elem)
            })

    # Si no hay incidencias
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
