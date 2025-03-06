from bs4 import BeautifulSoup
import re

def get_element_info(element):
    """Obtiene información útil del elemento HTML para facilitar la localización del error."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # Primeros 50 caracteres del texto
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"
    }

def check_focus_order(html_content, page_url):
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
                    "title": "Uso de tabindex mayor a 0",
                    "type": "Focus Order",
                    "severity": "High",
                    "description": f"El elemento tiene tabindex={tabindex_value}, lo que puede alterar el orden natural del foco.",
                    "remediation": "Evitar usar tabindex mayor a 0. Usa el orden natural del DOM.",
                    "wcag_reference": "2.4.3",
                    "impact": "El orden del foco puede volverse impredecible.",
                    "page_url": page_url,
                    "element_info": get_element_info(element)
                })
        
        # tabindex="-1" en elementos interactivos
        if str(tabindex_value) == "-1" and element.name in ["a", "button", "input", "textarea", "select"]:
            incidences.append({
                "title": "Elemento interactivo con tabindex=-1",
                "type": "Focus Order",
                "severity": "Medium",
                "description": "Un elemento interactivo tiene tabindex=-1, lo que lo hace inaccesible con Tab.",
                "remediation": "Evitar tabindex=-1 en elementos interactivos, salvo que se maneje con JavaScript.",
                "wcag_reference": "2.4.3",
                "impact": "Los usuarios no pueden acceder a este elemento con el teclado.",
                "page_url": page_url,
                "element_info": get_element_info(element)
            })

    # 2️⃣ Elementos interactivos que no son alcanzables con Tab
    interactive_elements = soup.find_all(["a", "button", "input", "textarea", "select"])
    for element in interactive_elements:
        if not element.has_attr("tabindex") and element.name == "a" and not element.has_attr("href"):
            incidences.append({
                "title": "Enlace sin href y sin tabindex",
                "type": "Focus Order",
                "severity": "Medium",
                "description": "Un enlace (<a>) sin href y sin tabindex no será accesible con el teclado.",
                "remediation": "Agregar un href o un tabindex=0 si debe ser enfocable.",
                "wcag_reference": "2.4.3",
                "impact": "El usuario de teclado no podrá acceder al enlace.",
                "page_url": page_url,
                "element_info": get_element_info(element)
            })

    # 3️⃣ Modales (dialog) que pueden no gestionar bien el foco
    dialogs = soup.find_all("dialog")
    for dialog in dialogs:
        if not dialog.has_attr("open"):
            incidences.append({
                "title": "Modal (dialog) sin atributo open",
                "type": "Focus Order",
                "severity": "Low",
                "description": "El elemento <dialog> no tiene el atributo 'open', lo que puede afectar el foco.",
                "remediation": "Asegurar que el diálogo tiene 'open' cuando está visible y maneja el foco correctamente.",
                "wcag_reference": "2.4.3",
                "impact": "Los usuarios podrían no notar que el modal está activo.",
                "page_url": page_url,
                "element_info": get_element_info(dialog)
            })

    return incidences
