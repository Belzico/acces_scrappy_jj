from bs4 import BeautifulSoup
import re

def get_element_info(element):
    """Obtiene información útil de un elemento HTML para facilitar la localización del error."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # Primeros 50 caracteres del texto
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"  # Obtiene el número de línea si es posible
    }

def check_info_and_relationships(html_content, page_url):
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
            "title": "Falta de encabezados semánticos",
            "type": "Structure",
            "severity": "Medium",
            "description": "No se encontraron etiquetas de encabezado (h1-h6).",
            "remediation": "Usar etiquetas h1-h6 en lugar de texto con estilos para indicar secciones.",
            "wcag_reference": "1.3.1",
            "impact": "Dificulta la navegación con lectores de pantalla.",
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
                "title": "Tabla con role='presentation' pero tiene <th>",
                "type": "Table Structure",
                "severity": "High",
                "description": "Se usa role='presentation' en una tabla con <th>, lo que puede ser confuso.",
                "remediation": "Eliminar role='presentation' si la tabla contiene datos estructurados.",
                "wcag_reference": "1.3.1",
                "impact": "Los lectores de pantalla pueden ignorar los encabezados de la tabla.",
                "page_url": page_url,
                "element_info": table_info
            })

        # Revisar si los encabezados <th> tienen 'scope' o están ligados con 'headers'
        for th in th_tags:
            th_info = get_element_info(th)
            if not th.has_attr("scope") and not th.has_attr("headers"):
                incidences.append({
                    "title": "Encabezado de tabla <th> sin 'scope' ni 'headers'",
                    "type": "Table Structure",
                    "severity": "Medium",
                    "description": "Un <th> no especifica 'scope' ni está asociado con 'headers'.",
                    "remediation": "Agregar scope='col' o scope='row', o relacionar con headers/id.",
                    "wcag_reference": "1.3.1",
                    "impact": "Los usuarios con lector de pantalla pueden no entender la relación entre celdas.",
                    "page_url": page_url,
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
                    "title": "Campo de formulario sin <label> ni ARIA",
                    "type": "Form Structure",
                    "severity": "High",
                    "description": "Un campo de formulario no tiene etiqueta asociada ni atributos ARIA.",
                    "remediation": "Agregar <label for='campo_id'>Texto</label> o usar aria-label/aria-labelledby.",
                    "wcag_reference": "1.3.1",
                    "impact": "Los usuarios con lector de pantalla no podrán entender la función del campo.",
                    "page_url": page_url,
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
                    "title": "Grupo de opciones sin <fieldset>",
                    "type": "Form Structure",
                    "severity": "Medium",
                    "description": f"El grupo de opciones '{group_name}' no está dentro de un <fieldset> con <legend>.",
                    "remediation": "Agrupar estos controles dentro de un <fieldset> con un <legend> descriptivo.",
                    "wcag_reference": "1.3.1",
                    "impact": "Los usuarios con lector de pantalla pueden no entender el propósito de las opciones.",
                    "page_url": page_url,
                    "element_info": field_info
                })

        # Verificar si el <fieldset> tiene un <legend>
        for field, fieldset in zip(fields, fieldset_parents):
            if fieldset and not fieldset.find("legend"):
                fieldset_info = get_element_info(fieldset)
                incidences.append({
                    "title": "Grupo de opciones sin <legend>",
                    "type": "Form Structure",
                    "severity": "Low",
                    "description": f"El grupo de opciones '{group_name}' tiene un <fieldset> pero le falta un <legend>.",
                    "remediation": "Agregar un <legend> dentro del <fieldset> para describir el propósito del grupo.",
                    "wcag_reference": "1.3.1",
                    "impact": "Los usuarios con lector de pantalla no podrán entender el propósito del grupo.",
                    "page_url": page_url,
                    "element_info": fieldset_info
                })

    return incidences
