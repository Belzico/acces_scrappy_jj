from bs4 import BeautifulSoup
import re

def get_element_info(element):
    """Obtiene información útil de un elemento HTML para facilitar la localización del error."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # Primeros 50 caracteres del texto
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"  # Número de línea si está disponible
    }

def check_focus_visible(html_content, page_url):
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
                "title": "Elemento sin indicador visible de foco",
                "type": "Focus Visibility",
                "severity": "High",
                "description": "El elemento usa estilos CSS que eliminan la visibilidad del foco.",
                "remediation": "Asegurar que el foco sea visible agregando `:focus` o `:focus-visible` en CSS.",
                "wcag_reference": "2.4.7",
                "impact": "Los usuarios de teclado no pueden ver qué elemento está enfocado.",
                "page_url": page_url,
                "element_info": element_info
            })

        # 2️⃣ Detectar elementos interactivos sin tabindex correcto
        if element.name in ["div", "span"] and ("onclick" in element.attrs or "role" in element.attrs):
            if "tabindex" not in element.attrs:
                incidences.append({
                    "title": "Elemento interactivo sin tabindex",
                    "type": "Focus Visibility",
                    "severity": "Medium",
                    "description": "Un elemento interactivo (div/span con onclick o role) no tiene `tabindex='0'`.",
                    "remediation": "Agregar `tabindex='0'` para que pueda recibir foco con teclado.",
                    "wcag_reference": "2.4.7",
                    "impact": "Los usuarios de teclado no pueden acceder a este elemento.",
                    "page_url": page_url,
                    "element_info": element_info
                })

        # 3️⃣ Detectar elementos con tabindex="-1" (los saca de la navegación)
        if "tabindex" in element.attrs and element.attrs["tabindex"] == "-1":
            incidences.append({
                "title": "Elemento con tabindex='-1'",
                "type": "Focus Visibility",
                "severity": "Medium",
                "description": "Un elemento tiene `tabindex='-1'`, lo que impide que reciba foco con el teclado.",
                "remediation": "Evitar `tabindex='-1'` a menos que haya una alternativa accesible.",
                "wcag_reference": "2.4.7",
                "impact": "El elemento no será accesible mediante teclado.",
                "page_url": page_url,
                "element_info": element_info
            })

        # 4️⃣ Detectar elementos que se ocultan al recibir foco
        if "display:none" in styles or "visibility:hidden" in styles:
            incidences.append({
                "title": "Elemento oculto al recibir foco",
                "type": "Focus Visibility",
                "severity": "High",
                "description": "El elemento desaparece al recibir foco (display: none o visibility: hidden).",
                "remediation": "Asegurar que el elemento permanezca visible cuando recibe foco.",
                "wcag_reference": "2.4.7",
                "impact": "Los usuarios pueden perder el contexto de navegación.",
                "page_url": page_url,
                "element_info": element_info
            })

    return incidences
