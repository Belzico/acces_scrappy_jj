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
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"  # Número de línea si está disponible
    }

def check_focus_visible(html_content, page_url,excel="issue_report.xlsx"):
    """
    Tester para WCAG 2.4.7 - Focus Visible.
    Detecta elementos interactivos que no tienen un indicador visible de foco o están mal configurados.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # Seleccionar elementos que pueden recibir foco o deberían poder recibirlo
    focusable_elements = soup.find_all(["a", "button", "input", "select", "textarea", "iframe", "div", "span"])

    for element in focusable_elements:
        element_info = get_element_info(element)
        styles = element.get("style", "").lower()

        # 1️⃣ Detectar si el foco está oculto con CSS
        if "outline:none" in styles or "outline: 0" in styles or "border: none" in styles:
            incidences.append({
    "title": "Element without visible focus indicator",
    "type": "Focus Visibility",
    "severity": "High",
    "description": "The element uses CSS styles that remove focus visibility.",
    "remediation": "Ensure focus is visible by adding `:focus` or `:focus-visible` in CSS.",
    "wcag_reference": "2.4.7",
    "impact": "Keyboard users cannot see which element is focused.",
    "page_url": page_url,
    "resolution": "check_focus_visible.md",
    "element_info": element_info
})


        # 2️⃣ Detectar elementos interactivos sin tabindex correcto
        if element.name in ["div", "span"] and ("onclick" in element.attrs or "role" in element.attrs):
            incidences.append({
    "title": "Interactive element without tabindex",
    "type": "Focus Visibility",
    "severity": "Medium",
    "description": "An interactive element (div/span with onclick or role) does not have `tabindex='0'`.",
    "remediation": "Add `tabindex='0'` so it can receive keyboard focus.",
    "wcag_reference": "2.4.7",
    "impact": "Keyboard users cannot access this element.",
    "page_url": page_url,
    "resolution": "check_focus_visible.md",
    "element_info": element_info
})


        # 3️⃣ Detectar elementos con tabindex="-1" (los saca de la navegación)
        if "tabindex" in element.attrs and element.attrs["tabindex"] == "-1":
            incidences.append({
    "title": "Element with tabindex='-1'",
    "type": "Focus Visibility",
    "severity": "Medium",
    "description": "An element has `tabindex='-1'`, preventing it from receiving keyboard focus.",
    "remediation": "Avoid using `tabindex='-1'` unless an accessible alternative is provided.",
    "wcag_reference": "2.4.7",
    "impact": "The element will not be accessible via keyboard.",
    "page_url": page_url,
    "resolution": "check_focus_visible.md",
    "element_info": element_info
})


        # 4️⃣ Detectar elementos que se ocultan al recibir foco
        if "display:none" in styles or "visibility:hidden" in styles:
           incidences.append({
    "title": "Element hidden when receiving focus",
    "type": "Focus Visibility",
    "severity": "High",
    "description": "The element disappears when it receives focus (display: none or visibility: hidden).",
    "remediation": "Ensure the element remains visible when it receives focus.",
    "wcag_reference": "2.4.7",
    "impact": "Users may lose navigation context.",
    "page_url": page_url,
    "resolution": "check_focus_visible.md",
    "element_info": element_info
})

    #Convertimos las incidencias directamente a Excel antes de retornar**
    transform_json_to_excel(incidences, excel)

    return incidences
