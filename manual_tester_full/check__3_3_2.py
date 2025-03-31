from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    """Extrae algunos metadatos del elemento."""
    return {
        "tag": element.name,
        "attrs": dict(element.attrs),
        "snippet": str(element)[:300]
    }

def format_incidence(inc):
    """Formatea la incidencia para exportar a Excel."""
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Check the form field identified below. There's no label or instruction."
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

def run_all___3_3_2(html_content, page_url, excel="issue_report.xlsx"):
    """
    Heurística:
    - Busca <input> (type != hidden/button/submit/reset/file), <select>, <textarea>
    - Ve si tienen label for=ID o aria-label/aria-labelledby o placeholder
    - Si no => error: Falta label/instrucción
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Tipos de input que normalmente requieren un label
    valid_input_types = [
        "text", "password", "email", "number", "search", "tel", "url", "date",
        "datetime-local", "month", "time", "week", "radio", "checkbox"
    ]

    # Hallar todos los campos relevantes
    form_fields = []

    # 1) <input> con type en valid_input_types
    inputs = soup.find_all("input")
    for inp in inputs:
        t = (inp.get("type") or "text").lower()
        if t in valid_input_types:
            form_fields.append(inp)

    # 2) <select>
    selects = soup.find_all("select")
    form_fields.extend(selects)

    # 3) <textarea>
    textareas = soup.find_all("textarea")
    form_fields.extend(textareas)

    # Buscar si hay <label for> que coincida o aria-label, aria-labelledby, placeholder
    for field in form_fields:
        field_id = field.get("id", "")
        has_label = False

        # Revisa <label for="field_id">
        if field_id:
            label = soup.find("label", {"for": field_id})
            if label and label.get_text(strip=True):
                has_label = True

        # Revisa aria-label o aria-labelledby
        aria_label = field.get("aria-label", "")
        aria_labelledby = field.get("aria-labelledby", "")

        if aria_label.strip():
            has_label = True
        if aria_labelledby.strip():
            # Podríamos buscar el texto en el elemento con ese id, pero
            # con que exista es buena pista
            has_label = True

        # Revisa placeholder (al menos una pista)
        placeholder = field.get("placeholder", "")
        if placeholder.strip():
            has_label = True

        if not has_label:
            raw_incidences.append({
                "title": "Form field without visible label or instructions",
                "type": "Labels or Instructions",
                "severity": "Medium",
                "expected_result": (
                    "Each input/select/textarea requiring user input must have a label or instructions."
                ),
                "actual_result": (
                    "No <label for>, no aria-label/aria-labelledby, no placeholder found."
                ),
                "remediation": (
                    "Add a <label> or instructions so the user knows what info to enter. "
                    "Alternatively, set aria-label or a placeholder as minimal fallback."
                ),
                "wcag_reference": "3.3.2",
                "impact": (
                    "Users, especially with cognitive disabilities, won't know what data is expected here."
                ),
                "page_url": page_url,
                "element_info": get_element_info(field)
            })

    # Si no se encontró incidencia
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
            "Failed checkpoint": "3.3.2",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
