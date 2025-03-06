from bs4 import BeautifulSoup
import re

def check_reflow_320px(html_content, page_url):
    """
    Detecta problemas de reflujo cuando la página se ve a 320px de ancho.
    
    🔹 Busca elementos con ancho fijo que pueden causar desbordamiento.
    🔹 Verifica si hay una barra de desplazamiento horizontal forzada.
    🔹 Analiza los estilos CSS embebidos en la página.
    🔹 Basado en WCAG 1.4.10: Reflow (https://www.w3.org/WAI/WCAG21/Understanding/reflow.html).

    Args:
        html_content (str): Contenido HTML de la página.
        page_url (str): URL (o identificador) de la página analizada.

    Returns:
        list[dict]: Lista de incidencias detectadas.
    """
    
    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 1) Buscar elementos con ancho fijo en estilos inline (`style="width: 600px;"`)
    problem_elements = []
    for tag in soup.find_all(style=True):
        style = tag["style"].lower()
        if re.search(r"width:\s*\d+px", style) and "max-width" not in style:
            problem_elements.append(tag)

    if problem_elements:
        incidences.append({
            "title": "Fixed width elements detected (inline styles)",
            "type": "Zoom",
            "severity": "High",
            "description": (
                "Se encontraron elementos con anchos fijos en píxeles dentro de atributos `style`, "
                "lo que puede impedir que el contenido fluya correctamente en un viewport de 320px."
            ),
            "remediation": (
                "Reemplazar anchos fijos (`width: 600px;`) por valores flexibles (`max-width: 100%`, `flexbox`, `grid`)."
            ),
            "wcag_reference": "1.4.10",
            "impact": "El usuario debe desplazarse horizontalmente para ver el contenido, dificultando la navegación.",
            "page_url": page_url,
        })

    # 🔍 2) Revisar estilos CSS embebidos en <style> dentro del <head>
    css_rules = []
    for style_tag in soup.find_all("style"):
        css_rules.extend(style_tag.get_text().split(";"))

    for rule in css_rules:
        if re.search(r"width:\s*\d+px", rule) and "max-width" not in rule:
            incidences.append({
                "title": "Fixed width detected in CSS",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    "Se detectó un `width: Xpx` en los estilos CSS de la página sin `max-width`, "
                    "lo que puede impedir que el contenido fluya correctamente en un viewport de 320px."
                ),
                "remediation": (
                    "Evitar `width: Xpx;` y usar `max-width: 100%` o CSS flexible con `grid` o `flexbox`."
                ),
                "wcag_reference": "1.4.10",
                "impact": "El usuario no puede ver el contenido sin desplazarse horizontalmente, lo cual es una mala práctica en móviles.",
                "page_url": page_url,
            })

    # 🔍 3) Verificar si se fuerza el desplazamiento horizontal con `overflow-x`
    for tag in soup.find_all(style=True):
        style = tag["style"].lower()
        if "overflow-x: auto" in style or "overflow-x: scroll" in style:
            incidences.append({
                "title": "Horizontal scrolling detected",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    "Se detectó una barra de desplazamiento horizontal en la página, lo que indica "
                    "que el contenido no se ajusta correctamente al viewport de 320px."
                ),
                "remediation": (
                    "Modificar los contenedores para usar `max-width: 100%` y evitar `overflow-x: scroll`."
                ),
                "wcag_reference": "1.4.10",
                "impact": "El usuario no puede ver el contenido sin desplazarse horizontalmente, lo cual es una mala práctica en móviles.",
                "page_url": page_url,
            })
    
    return incidences
