from bs4 import BeautifulSoup

def check_menu_text_spacing(html_content, page_url):
    """
    Detecta si los elementos del menú se desbordan o quedan cortados cuando se ajusta el espaciado del texto.

    🔹 Basado en WCAG 1.4.12: Text Spacing.
    🔹 Busca problemas de `overflow: hidden;`, `white-space: nowrap;` y `max-height` en menús.
    🔹 Identifica si el texto de los elementos de menú se sale del contenedor o es ilegible.

    Args:
        html_content (str): Contenido HTML de la página.
        page_url (str): URL de la página analizada.

    Returns:
        list[dict]: Lista de incidencias detectadas.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 Buscar todos los elementos de navegación que puedan contener menús
    menus = soup.find_all(["nav", "ul", "div"], class_=["menu", "navigation", "navbar"])

    for menu in menus:
        # 🔍 Revisar estilos que podrían causar problemas con espaciado
        for item in menu.find_all(["li", "a", "span", "div"]):
            style = item.get("style", "").lower()

            if "overflow: hidden" in style:
                incidences.append({
                    "title": "Content may be cropped with text spacing adjustments",
                    "type": "Zoom",
                    "severity": "High",
                    "description": (
                        "Se detectó `overflow: hidden;` en un elemento del menú. "
                        "Esto puede hacer que el contenido se recorte al aumentar el espaciado de texto."
                    ),
                    "remediation": (
                        "Evitar `overflow: hidden;` en elementos de menú. "
                        "Permitir que el contenido se expanda correctamente."
                    ),
                    "wcag_reference": "1.4.12",
                    "impact": "Usuarios que necesiten espaciado adicional podrían no ver todo el contenido.",
                    "page_url": page_url,
                })

            if "white-space: nowrap" in style:
                incidences.append({
                    "title": "Text does not wrap in the menu",
                    "type": "Zoom",
                    "severity": "High",
                    "description": (
                        "Se detectó `white-space: nowrap;`, lo que impide que el texto se ajuste correctamente "
                        "al aumentar el espaciado de texto."
                    ),
                    "remediation": (
                        "Evitar `white-space: nowrap;` en menús para que el texto pueda ajustarse correctamente."
                    ),
                    "wcag_reference": "1.4.12",
                    "impact": "Los elementos del menú podrían salirse de su contenedor.",
                    "page_url": page_url,
                })

            if "max-height" in style and "px" in style:
                incidences.append({
                    "title": "Menu items may be cut off",
                    "type": "Zoom",
                    "severity": "High",
                    "description": (
                        "Se detectó `max-height` en píxeles en un menú, lo que puede hacer que los elementos "
                        "se recorten cuando el espaciado del texto aumente."
                    ),
                    "remediation": (
                        "Usar `min-height: auto;` en lugar de valores fijos para permitir ajuste dinámico."
                    ),
                    "wcag_reference": "1.4.12",
                    "impact": "El usuario podría no ver todo el contenido del menú.",
                    "page_url": page_url,
                })

    return incidences
