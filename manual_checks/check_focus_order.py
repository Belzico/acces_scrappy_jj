from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel  

def get_element_info(element):
    """Obtiene información útil del elemento HTML para facilitar la localización del error."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # Primeros 50 caracteres del texto
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"
    }

def check_focus_order(html_content, page_url,excel="issue_report.xlsx"):
    """
    Tester para WCAG 2.4.3 - Focus Order.
    Detecta problemas de navegación del foco en HTML.
    """
    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 1️⃣ Elementos con tabindex > 0 (puede romper el orden de foco)
    elements_with_tabindex = soup.find_all(lambda tag: tag.has_attr("tabindex"))
    for element in elements_with_tabindex:
        tabindex_value = element.get("tabindex")
        if tabindex_value and tabindex_value.isdigit():
            tabindex_value = int(tabindex_value)
            if tabindex_value > 0:
                incidences.append({
    "title": "Use of tabindex greater than 0",
    "type": "Focus Order",
    "severity": "High",
    "description": f"The element has tabindex={tabindex_value}, which can disrupt the natural focus order.",
    "remediation": "Avoid using tabindex greater than 0. Use the natural DOM order.",
    "wcag_reference": "2.4.3",
    "impact": "The focus order may become unpredictable.",
    "page_url": page_url,
    "resolution":"check_focus_order.md",
    "element_info": get_element_info(element)
})

        
        # tabindex="-1" en elementos interactivos
        if str(tabindex_value) == "-1" and element.name in ["a", "button", "input", "textarea", "select"]:
            incidences.append({
    "title": "Interactive element with tabindex=-1",
    "type": "Focus Order",
    "severity": "Medium",
    "description": "An interactive element has tabindex=-1, making it inaccessible via the Tab key.",
    "remediation": "Avoid using tabindex=-1 on interactive elements unless managed with JavaScript.",
    "wcag_reference": "2.4.3",
    "impact": "Users cannot access this element using the keyboard.",
    "page_url": page_url,
    "resolution":"check_focus_order.md",
    "element_info": get_element_info(element)
})


    # 2️⃣ Elementos interactivos que no son alcanzables con Tab
    interactive_elements = soup.find_all(["a", "button", "input", "textarea", "select"])
    for element in interactive_elements:
        if not element.has_attr("tabindex") and element.name == "a" and not element.has_attr("href"):
            incidences.append({
    "title": "Link without href and without tabindex",
    "type": "Focus Order",
    "severity": "Medium",
    "description": "A link (<a>) without an href and without a tabindex will not be accessible via the keyboard.",
    "remediation": "Add an href or a tabindex=0 if it needs to be focusable.",
    "wcag_reference": "2.4.3",
    "impact": "Keyboard users will not be able to access the link.",
    "page_url": page_url,
    "resolution":"check_focus_order.md",
    "element_info": get_element_info(element)
})

    # 3️⃣ Modales (dialog) que pueden no gestionar bien el foco
    dialogs = soup.find_all("dialog")
    for dialog in dialogs:
        if not dialog.has_attr("open"):
            incidences.append({
    "title": "Modal (dialog) without 'open' attribute",
    "type": "Focus Order",
    "severity": "Low",
    "description": "The <dialog> element does not have the 'open' attribute, which may affect focus behavior.",
    "remediation": "Ensure the dialog has the 'open' attribute when visible and correctly manages focus.",
    "wcag_reference": "2.4.3",
    "impact": "Users may not realize that the modal is active.",
    "page_url": page_url,
    "resolution":"check_focus_order.md",
    "element_info": get_element_info(dialog)
})

    #Convertimos las incidencias directamente a Excel antes de retornar**
    transform_json_to_excel(incidences, excel)
    
    return incidences
