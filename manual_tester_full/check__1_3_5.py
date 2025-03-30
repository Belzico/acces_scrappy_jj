from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

VALID_AUTOCOMPLETE_VALUES = {
    "name", "honorific-prefix", "given-name", "additional-name", "family-name", "honorific-suffix",
    "nickname", "username", "new-password", "current-password", "organization-title", "organization",
    "street-address", "address-line1", "address-line2", "address-line3", "address-level4",
    "address-level3", "address-level2", "address-level1", "country", "country-name", "postal-code",
    "cc-name", "cc-given-name", "cc-additional-name", "cc-family-name", "cc-number", "cc-exp",
    "cc-exp-month", "cc-exp-year", "cc-csc", "cc-type", "transaction-currency", "transaction-amount",
    "language", "bday", "bday-day", "bday-month", "bday-year", "sex", "url", "photo", "tel",
    "tel-country-code", "tel-national", "tel-area-code", "tel-local", "tel-local-prefix",
    "tel-local-suffix", "tel-extension", "email", "impp", "shipping", "billing"
}

def get_element_info(element):
    """
    Devuelve un diccionario con información contextual
    (tag, id, class, line_number y evidence) de un elemento HTML.
    """
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    evidence_parts = []
    if classes:
        evidence_parts.append(f"class={classes}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")

    evidence = f"{tag}[{', '.join(evidence_parts)}]" if evidence_parts else tag

    return {
        "tag": tag,
        "text": element.get("value", "")[:50] or element.get("placeholder", "")[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }

def format_incidence(inc):
    """
    Formatea la información de la incidencia en un diccionario
    listo para exportar a Excel.
    """
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the form element: {inc.get('element_info', {}).get('tag', 'N/A')}.\n"
            "3. Check whether `autocomplete` is present and has a valid value."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "N/A")
    }

def run_all___1_3_5(html_content, page_url, excel="issue_report.xlsx"):
    """
    1. Parsea el contenido HTML con BeautifulSoup
    2. Busca los <input> (y potencialmente podrías expandir a <textarea>, <select>, etc.)
    3. Aplica una heurística para identificar inputs relacionados con datos personales.
    4. Verifica la presencia y validez del atributo 'autocomplete'.
    5. Genera incidencias para los casos de error y las exporta a Excel.
    6. Retorna la lista formateada de incidencias (cada incidencia es un dict).
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Encuentra todos los inputs
    inputs = soup.find_all("input")
    
    # Heurística: palabras clave que pueden indicar datos personales
    relevant_keywords = [
        "name", "email", "user", "tel", "phone", "address",
        "bday", "birth", "pass", "zip", "code"
    ]

    for element in inputs:
        input_type = element.get("type", "text").lower()
        autocomplete = element.get("autocomplete")
        name_attr = element.get("name", "").lower()

        info = get_element_info(element)

        # Decide si es un input relevante para 1.3.5
        # Primero: excluir inputs poco relevantes (ocultos, etc.)
        if input_type in ["hidden", "button", "submit", "reset", "checkbox", "radio", "file"]:
            continue

        # Segundo: comprueba si alguno de los keywords aparece en el name
        if any(keyword in name_attr for keyword in relevant_keywords):
            # Check: si no tiene autocomplete => error
            if not autocomplete:
                raw_incidences.append({
                    "title": "Input collecting user data is missing `autocomplete`",
                    "type": "Form Semantics",
                    "severity": "Medium",
                    "expected_result": "Inputs collecting user data must include `autocomplete` with a valid value.",
                    "actual_result": "`autocomplete` attribute is missing.",
                    "remediation": (
                        "Add a valid `autocomplete` attribute, por ejemplo: "
                        "'email', 'given-name', 'tel', 'postal-code', etc."
                    ),
                    "wcag_reference": "1.3.5",
                    "impact": "Assistive technologies cannot infer the purpose of this input.",
                    "page_url": page_url,
                    "element_info": info
                })
            else:
                # Si tiene autocomplete, pero no es un valor válido => error
                if autocomplete not in VALID_AUTOCOMPLETE_VALUES:
                    raw_incidences.append({
                        "title": "Input uses invalid `autocomplete` value",
                        "type": "Form Semantics",
                        "severity": "Low",
                        "expected_result": (
                            "The value of `autocomplete` must be one of the "
                            "standard HTML 5.2 values."
                        ),
                        "actual_result": f"`autocomplete=\"{autocomplete}\"` is not a valid value.",
                        "remediation": (
                            "Replace with a valid `autocomplete` value, como "
                            "'nickname', 'email', 'given-name', 'bday', etc."
                        ),
                        "wcag_reference": "1.3.5",
                        "impact": (
                            "Browsers may ignore this value and not help users "
                            "fill out the form correctly."
                        ),
                        "page_url": page_url,
                        "element_info": info
                    })

    # Formateamos y exportamos a Excel
    formatted = [format_incidence(i) for i in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)
    
    return formatted
