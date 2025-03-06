from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel  

def get_element_info(element):
    """Obtiene información útil de un elemento HTML para facilitar la localización del error."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # Primeros 50 caracteres del texto
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"  # Obtiene el número de línea si es posible
    }

def check_info_and_relationships(html_content, page_url,excel="issue_report.xlsx"):
    """
    Tester mejorado para WCAG 2.2 - Criterio 1.3.1 (Info and Relationships).
    Ahora proporciona detalles más precisos sobre la ubicación del error.
    """
    
    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 1️⃣ ENCABEZADOS (h1-h6) → Si faltan encabezados semánticos
    heading_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if not heading_tags:
        incidences.append({
    "title": "Missing semantic headings",
    "type": "Structure",
    "severity": "Medium",
    "description": "No heading tags (h1-h6) were found.",
    "remediation": "Use h1-h6 tags instead of styled text to indicate sections.",
    "wcag_reference": "1.3.1",
    "impact": "Makes navigation difficult for screen reader users.",
    "resolution":"check_info_and_relationships.md",
    "page_url": page_url
})


    # 2️⃣ TABLAS → Si no tienen <th> o relaciones programáticas adecuadas
    tables = soup.find_all("table")
    for table in tables:
        table_info = get_element_info(table)
        th_tags = table.find_all("th")

        # Tabla con role="presentation" pero contiene <th> → Error
        if table.get("role", "").lower() in ["presentation", "none"] and th_tags:
            incidences.append({
    "title": "Table with role='presentation' contains <th>",
    "type": "Table Structure",
    "severity": "High",
    "description": "A table uses role='presentation' but contains <th>, which can be confusing.",
    "remediation": "Remove role='presentation' if the table contains structured data.",
    "wcag_reference": "1.3.1",
    "impact": "Screen readers may ignore table headers.",
    "page_url": page_url,
    "resolution":"check_info_and_relationships.md",
    "element_info": table_info
})


        # Revisar si los encabezados <th> tienen 'scope' o están ligados con 'headers'
        for th in th_tags:
            th_info = get_element_info(th)
            if not th.has_attr("scope") and not th.has_attr("headers"):
                incidences.append({
    "title": "Table header <th> missing 'scope' and 'headers'",
    "type": "Table Structure",
    "severity": "Medium",
    "description": "A <th> element does not specify 'scope' or is not associated with 'headers'.",
    "remediation": "Add scope='col' or scope='row', or associate with headers/id.",
    "wcag_reference": "1.3.1",
    "impact": "Screen reader users may not understand the relationship between table cells.",
    "page_url": page_url,
    "resolution":"check_info_and_relationships.md",
    "element_info": th_info
})


    # 3️⃣ FORMULARIOS → Si los campos de entrada no tienen etiquetas asociadas
    forms = soup.find_all("form")
    for form in forms:
        form_fields = form.find_all(["input", "select", "textarea"])
        for field in form_fields:
            if field.name == "input" and field.get("type", "").lower() in ["submit", "reset", "button", "image"]:
                continue  # Ignorar botones

            field_info = get_element_info(field)
            field_id = field.get("id")
            has_label = False

            # Buscar etiqueta <label for="id">
            if field_id:
                label = form.find("label", attrs={"for": field_id})
                if label:
                    has_label = True

            # Buscar atributos ARIA
            aria_label = field.get("aria-label")
            aria_labelledby = field.get("aria-labelledby")
            if aria_label or aria_labelledby:
                has_label = True

            # Si no tiene etiqueta ni atributos ARIA, generar incidencia
            if not has_label:
                incidences.append({
    "title": "Form field missing <label> and ARIA",
    "type": "Form Structure",
    "severity": "High",
    "description": "A form field has no associated label or ARIA attributes.",
    "remediation": "Add <label for='field_id'>Text</label> or use aria-label/aria-labelledby.",
    "wcag_reference": "1.3.1",
    "impact": "Screen reader users may not understand the purpose of the field.",
    "page_url": page_url,
    "resolution":"check_info_and_relationships.md",
    "element_info": field_info
})


    # 4️⃣ DETECCIÓN DE GRUPOS DE RADIO Y CHECKBOX SIN FIELDSET Y LEGEND
    radio_checkbox_groups = {}
    for field in soup.find_all("input", {"type": ["radio", "checkbox"]}):
        name = field.get("name")
        if name:
            if name not in radio_checkbox_groups:
                radio_checkbox_groups[name] = []
            radio_checkbox_groups[name].append(field)

    for group_name, fields in radio_checkbox_groups.items():
        # Verificar si los elementos están dentro de un <fieldset>
        fieldset_parents = [field.find_parent("fieldset") for field in fields]
        fieldset_parent = any(fieldset_parents)
        
        if not fieldset_parent:
            for field in fields:
                field_info = get_element_info(field)
                incidences.append({
                "title": "Option group missing <fieldset>",
                "type": "Form Structure",
                "severity": "Medium",
                "description": f"The option group '{group_name}' is not inside a <fieldset> with a <legend>.",
                "remediation": "Group these controls inside a <fieldset> with a descriptive <legend>.",
                "wcag_reference": "1.3.1",
                "impact": "Screen reader users may not understand the purpose of the options.",
                "page_url": page_url,
                "resolution":"check_info_and_relationships.md",
                "element_info": field_info
            })


    #Convertimos las incidencias directamente a Excel antes de retornar**
    transform_json_to_excel(incidences, excel)

    return incidences  # 📌 El Excel ya se ha generado antes de retornar
