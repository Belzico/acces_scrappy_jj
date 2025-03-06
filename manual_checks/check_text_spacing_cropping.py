import re
from bs4 import BeautifulSoup

def check_text_spacing_cropping(html_content, page_url):
    """
    Detecta si el contenido se recorta cuando se aplican reglas de espaciado de texto accesible (WCAG 1.4.12).
    Verifica contenedores con `overflow: hidden;` y alturas fijas en estilo inline.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 1) Buscar elementos (p, div, span, etc.) con estilo inline
    text_containers = soup.find_all(["p", "div", "span", "section", "article"], style=True)

    # Expresión regular que busca `overflow: hidden;`, `overflow-x: hidden;` o `overflow-y: hidden;`
    # ignorando mayúsculas/minúsculas y espacios opcionales.
    overflow_hidden_regex = re.compile(r"overflow(?:-x|-y)?\s*:\s*hidden", re.IGNORECASE)

    # Expresión regular que busca `height` fijo en píxeles
    height_fixed_regex = re.compile(r"height\s*:\s*\d+px", re.IGNORECASE)

    for element in text_containers:
        style_attr = element["style"].lower()

        # 2) Detectar `overflow: hidden;` (en todas sus variantes)
        if overflow_hidden_regex.search(style_attr):
            incidences.append({
                "title": "Content may be cropped with text spacing adjustments",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    "Se detectó `overflow: hidden;` (o variante -x/-y) en un contenedor de texto. "
                    "Esto puede hacer que el contenido se recorte al aumentar el espaciado."
                ),
                "remediation": (
                    "Evitar `overflow: hidden;` en contenedores de texto cuando se aplica espaciado adicional. "
                    "Usar `overflow: visible;` o permitir expansión dinámica."
                ),
                "wcag_reference": "1.4.12",
                "impact": "Usuarios que necesiten espaciado adicional podrían no ver todo el contenido.",
                "page_url": page_url,
            })

        # 3) Detectar altura fija en px
        if height_fixed_regex.search(style_attr):
            incidences.append({
                "title": "Fixed height detected, may crop text",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    "Se detectó una altura fija en píxeles (`height: XXXpx;`) en un contenedor de texto. "
                    "Esto puede impedir que el texto se ajuste cuando se aplique espaciado extra."
                ),
                "remediation": (
                    "Usar `min-height: auto;` en lugar de alturas fijas para permitir la expansión dinámica."
                ),
                "wcag_reference": "1.4.12",
                "impact": "El texto puede quedar cortado cuando el usuario amplía y agrega espaciado.",
                "page_url": page_url,
            })

    return incidences
