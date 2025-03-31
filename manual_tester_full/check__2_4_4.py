from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

# Texto de enlace ambiguo o demasiado genérico
AMBIGUOUS_LINK_TEXT = [
    "click here", "here", "more", "read more", "read more...", "learn more",
    "ver más", "hacer clic aquí", "pulsa aquí", "aquí", "ver más..."
]

def get_element_info(element):
    return {
        "tag": element.name,
        "text": element.get_text(strip=True),
        "evidence": str(element)[:300]
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the link with text: \"{inc.get('element_info', {}).get('text')}\"."
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

def run_all___2_4_4(html_content, page_url, excel="issue_report.xlsx"):
    """
    Verifica que el texto de los enlaces sea lo suficientemente descriptivo.
    Identifica como incidencias:
      - Enlaces con texto vacío
      - Enlaces con texto ambiguo ("click here", "read more", etc.)
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Encontrar todos los enlaces
    all_links = soup.find_all("a")
    
    for link in all_links:
        link_text = link.get_text(strip=True)
        lower_text = link_text.lower()

        # 1) Si un <a> no tiene texto ni contenido alt => Error
        if not link_text:
            raw_incidences.append({
                "title": "Link text is empty",
                "type": "Link Purpose",
                "severity": "High",
                "expected_result": "Links must have accessible text indicating their purpose.",
                "actual_result": "Found a link (<a>) with no link text.",
                "remediation": "Add descriptive text between <a>...</a> or use aria-label/title if it's an icon link.",
                "wcag_reference": "2.4.4",
                "impact": (
                    "Screen reader or keyboard-only users cannot determine the purpose of the link."
                ),
                "page_url": page_url,
                "element_info": get_element_info(link)
            })
            continue

        # 2) Si el texto está en la lista de ambiguos => Error
        if lower_text in AMBIGUOUS_LINK_TEXT:
            raw_incidences.append({
                "title": "Ambiguous or generic link text",
                "type": "Link Purpose",
                "severity": "Medium",
                "expected_result": "Links must describe their purpose in context.",
                "actual_result": f"The link text is too generic: \"{link_text}\"",
                "remediation": (
                    "Use specific text, e.g. 'Download the annual report' instead of 'click here'. "
                    "Or ensure the link is accompanied by contextual text on the same line/paragraph."
                ),
                "wcag_reference": "2.4.4",
                "impact": (
                    "Users who browse links out of context (e.g., with a screen reader) "
                    "cannot discern the purpose of the link."
                ),
                "page_url": page_url,
                "element_info": get_element_info(link)
            })

    # Si no encontramos incidencias, añadimos la justificación
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
            "Failed checkpoint": "2.4.4",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
