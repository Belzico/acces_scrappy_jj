from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

# Palabras o frases comunes en mensajes de estado
POSSIBLE_STATUS_KEYWORDS = [
    "error", "invalid", "fail", "failed", "warning",
    "success", "successfully", "results returned", "added to", "items in cart",
    "loading", "please wait", "no results", "busy", "completed", "submitted"
]

# Atributos/roles ARIA que podrían identificar un status message
VALID_STATUS_ROLES = {
    "status", "alert", "log", "progressbar"
}
VALID_LIVE_VALUES = {
    "polite", "assertive"
}

def get_element_info(element):
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:120],
        "evidence": str(element)[:300]
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Inspect the text that appears to be a status message."
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

def is_status_role(element):
    """Revisa si el elemento o alguno de sus padres tiene un rol/status ARIA."""
    role_attr = element.get("role", "")
    aria_live = element.get("aria-live", "")

    if role_attr in VALID_STATUS_ROLES:
        return True
    if aria_live in VALID_LIVE_VALUES:
        return True

    # Verificar ancestros (subir en el árbol hasta body)
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
    - Busca fragmentos de texto (p, div, span, etc.) que contengan keywords
      típicas de mensajes de estado (como "error", "success", "loading"...).
    - Verifica si el elemento (o un ancestro) está marcado con role="status",
      role="alert", aria-live="polite"/"assertive", etc.
    - Si no se encuentra nada de eso => Incidencia.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Buscar elementos de texto comunes
    # Podrías ampliar a h1..h6 o strong, etc. si esperas mensajes ahí también
    possible_text_blocks = soup.find_all(["p", "div", "span", "li", "section"])

    for elem in possible_text_blocks:
        text_lower = elem.get_text(strip=True).lower()

        # Verificar si hay keywords
        if any(kw in text_lower for kw in POSSIBLE_STATUS_KEYWORDS):
            # Chequear si ya está marcado con role= o aria-live=...
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
                    "element_info": get_element_info(elem)
                })

    # Si no encontró incidencias
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
