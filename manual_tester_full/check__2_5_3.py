from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:80],
        "evidence": str(element)[:300]
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the element \"{inc.get('element_info', {}).get('tag')}\"."
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

def run_all___2_5_3(html_content, page_url, excel="issue_report.xlsx"):
    """
    Heurística para verificar que, si un control tiene texto visible,
    ese texto aparezca (parcialmente) en su accesible name (ej. aria-label).
    
    - <button> => Usa text content si no hay aria-label
    - <input type='button|submit|reset|image'> => Usa value o alt
    - <label> + <input> => Usa el texto de <label> y revisa aria-label del <input>
    
    Si el texto visible no figura en el aria-label / alt / value, se reporta.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 1) Revisar <button>
    buttons = soup.find_all("button")
    for btn in buttons:
        visible_text = btn.get_text(strip=True)
        aria_label = btn.get("aria-label", "")
        # Nombre accesible real: si aria-label existe, se suele imponer.
        # Si no hay aria-label, el user agent usa el texto interno del <button>.
        # Reglas simplificadas:
        if aria_label:
            # Si el visible text no está contenido en aria_label => error
            if visible_text and visible_text.lower() not in aria_label.lower():
                raw_incidences.append({
                    "title": "Button label mismatch",
                    "type": "Label in Name",
                    "severity": "Medium",
                    "expected_result": (
                        "The visible text of the button should be included in the aria-label."
                    ),
                    "actual_result": (
                        f"Visible: '{visible_text}', aria-label: '{aria_label}'"
                    ),
                    "remediation": (
                        "Ensure aria-label includes the visible text or remove aria-label if unneeded."
                    ),
                    "wcag_reference": "2.5.3",
                    "impact": (
                        "Voice users may say the visible text and fail to activate the button."
                    ),
                    "page_url": page_url,
                    "element_info": get_element_info(btn)
                })
        else:
            # If there's no aria-label, we rely on visible text => 
            # if there's no visible text => error
            if not visible_text:
                raw_incidences.append({
                    "title": "Button has no visible label nor aria-label",
                    "type": "Label in Name",
                    "severity": "High",
                    "expected_result": (
                        "Buttons must have a visible text or an aria-label that matches it."
                    ),
                    "actual_result": "No text and no aria-label found.",
                    "remediation": "Add text inside the button or set an aria-label attribute.",
                    "wcag_reference": "2.5.3",
                    "impact": (
                        "Users (especially voice input) cannot identify or activate the button by name."
                    ),
                    "page_url": page_url,
                    "element_info": get_element_info(btn)
                })

    # 2) Revisar <input type="button|submit|reset|image">
    inputs = soup.find_all("input", {"type": ["button", "submit", "reset", "image"]})
    for inp in inputs:
        value_text = inp.get("value", "")
        aria_label = inp.get("aria-label", "")
        alt_text   = inp.get("alt", "")  # para type="image"

        # Determinar "visible" text heurístico:
        # - Si type=image, el visible text a menudo es un icono. Su "texto" vendría de alt
        # - Si type=button|submit|reset, el visible text vendría del "value"
        #   (lo que aparece como texto del botón, si no, se ve un genérico)
        if inp.get("type") == "image":
            # "visible_text" se asume = alt_text
            # => si aria-label existe, preferirlo => se necesita que alt esté contenido
            visible_text = alt_text
        else:
            visible_text = value_text

        # Nombre accesible preferente: aria-label si existe
        # Si no => alt (para image) o value (para button/submit).
        if aria_label:
            # Chequeo: visible_text debe estar dentro de aria_label
            if visible_text and visible_text.lower() not in aria_label.lower():
                raw_incidences.append({
                    "title": "Input button label mismatch",
                    "type": "Label in Name",
                    "severity": "Medium",
                    "expected_result": (
                        "The visible text of the input should be included in the aria-label."
                    ),
                    "actual_result": f"Visible: '{visible_text}', aria-label: '{aria_label}'",
                    "remediation": (
                        "Ensure aria-label includes the visible text or remove aria-label if unneeded."
                    ),
                    "wcag_reference": "2.5.3",
                    "impact": "Voice input users may say the visible text and fail to activate the control.",
                    "page_url": page_url,
                    "element_info": get_element_info(inp)
                })
        else:
            # if no aria-label => we rely on alt (for image) or value
            # if there's no "visible" text => error
            if not visible_text:
                raw_incidences.append({
                    "title": "Input button has no visible text nor aria-label",
                    "type": "Label in Name",
                    "severity": "High",
                    "expected_result": "A button or image input must have a label for users.",
                    "actual_result": "No 'value', no 'alt', and no 'aria-label'.",
                    "remediation": "Add a 'value' (for type=button,submit,reset), alt text (for type=image), or aria-label.",
                    "wcag_reference": "2.5.3",
                    "impact": "Users cannot invoke the control by voice command using the visible label.",
                    "page_url": page_url,
                    "element_info": get_element_info(inp)
                })

    # 3) Revisar si un <label> está asociado a un <input> y si hay aria-label distinto
    #    Esto es muy simplificado: asume label for=ID => match input id=ID
    labels = soup.find_all("label")
    for lbl in labels:
        label_text = lbl.get_text(strip=True)
        if not label_text:
            # Un label vacío ya es problema, pero no de este SC (sería 2.4.6)
            continue

        # Hallar el input asociado, si "for" se usa
        for_id = lbl.get("for")
        if for_id:
            input_el = soup.find(id=for_id)
            if input_el:
                # si input_el tiene aria-label, debe contener label_text
                aria_label = input_el.get("aria-label", "")
                if aria_label and label_text.lower() not in aria_label.lower():
                    raw_incidences.append({
                        "title": "Form label mismatch",
                        "type": "Label in Name",
                        "severity": "Medium",
                        "expected_result": "The visible label text should be included in the aria-label.",
                        "actual_result": f"Label text: '{label_text}', aria-label: '{aria_label}'",
                        "remediation": (
                            "Match them (or remove aria-label if the label element is correctly associated)."
                        ),
                        "wcag_reference": "2.5.3",
                        "impact": "Voice users might try to refer to the input as 'label text' but not be recognized.",
                        "page_url": page_url,
                        "element_info": get_element_info(input_el)
                    })

    # 4) Generar el reporte final
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
            "Failed checkpoint": "2.5.3",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
