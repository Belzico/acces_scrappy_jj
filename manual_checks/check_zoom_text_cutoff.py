from bs4 import BeautifulSoup

def check_zoom_text_cutoff(html_content, page_url):
    """
    Detecta si el texto se corta al hacer zoom al 200%.
    
    🔹 Revisa `overflow: hidden`, `height`, `max-height` en CSS inline.
    🔹 Busca clases problemáticas que puedan ocultar contenido con `hidden`, `truncate`, etc.
    🔹 Basado en WCAG 1.4.4: Resize Text (https://www.w3.org/WAI/WCAG21/Understanding/resize-text.html).

    Args:
        html_content (str): Contenido HTML de la página.
        page_url (str): URL de la página analizada.

    Returns:
        list[dict]: Lista de incidencias detectadas.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 1) Buscar estilos en línea que pueden causar recorte de texto
    problem_elements = []
    for tag in soup.find_all(style=True):
        style = tag["style"].lower()
        if "overflow: hidden" in style or "height:" in style or "max-height:" in style:
            problem_elements.append(tag)

    if problem_elements:
        incidences.append({
            "title": "Text may be cut off at 200% zoom",
            "type": "Zoom",
            "severity": "High",
            "description": (
                "Se detectaron elementos con `overflow: hidden;`, `height` o `max-height` fijos, lo que puede "
                "ocultar contenido cuando la página se amplía al 200%."
            ),
            "remediation": (
                "Asegurar que los contenedores puedan expandirse dinámicamente al aumentar el tamaño del texto. "
                "Evitar `overflow: hidden;` en secciones de contenido crítico y usar `min-height` en lugar de `height`."
            ),
            "wcag_reference": "1.4.4",
            "impact": "El usuario podría perder información importante al hacer zoom.",
            "page_url": page_url,
        })

    # 🔍 2) Buscar clases comunes que pueden truncar texto
    problematic_classes = {"hidden", "truncate", "text-cutoff", "text-hidden"}
    for tag in soup.find_all(class_=True):
        classes = set(tag["class"])
        if classes & problematic_classes:
            incidences.append({
                "title": "Text truncation detected",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    f"Se detectaron clases `{classes & problematic_classes}` que pueden truncar texto, "
                    "evitando que sea visible cuando el usuario amplía al 200%."
                ),
                "remediation": (
                    "Asegurar que el contenido completo sea visible y accesible sin necesidad de desplazamiento horizontal."
                ),
                "wcag_reference": "1.4.4",
                "impact": "El texto puede quedar oculto sin que el usuario pueda acceder a él.",
                "page_url": page_url,
            })

    return incidences
