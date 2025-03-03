from bs4 import BeautifulSoup

def check_buttons_only_by_color(html_content, page_url):
    """
    Verifica si los botones y enlaces se identifican únicamente por su color.

    - Busca `<button>` y `<a>` en la página.
    - Verifica si tienen estilos como `text-decoration: underline`, `border` o `background-color`.
    - Si solo usan color sin pistas visuales adicionales, genera una incidencia.
    """

    # 1) Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Buscar todos los botones y enlaces
    elements = soup.find_all(["button", "a"])

    # 3) Identificar elementos sin subrayado, borde o fondo que dependan solo del color
    problematic_elements = []
    for element in elements:
        style = element.get("style", "").lower()
        
        # Condiciones que verifican si el elemento usa solo color
        uses_only_color = (
            "text-decoration: underline" not in style and
            "border" not in style and
            "background-color" not in style
        )

        # Si cumple la condición, lo agregamos a la lista
        if uses_only_color:
            problematic_elements.append(element)

    # 4) Generar incidencias si hay elementos que dependen solo del color
    incidencias = []
    if problematic_elements:
        incidencias.append({
            "title": "Multiple buttons/links identified only by use of color",
            "type": "Color",
            "severity": "Low",
            "description": (
                "Algunos botones o enlaces solo se identifican por su color sin pistas visuales adicionales. "
                "Los usuarios con discapacidad visual pueden no reconocerlos correctamente."
            ),
            "remediation": (
                "Añadir pistas visuales como `text-decoration: underline` en enlaces, `border` en botones o "
                "negrita en el texto para diferenciarlos del contenido normal."
            ),
            "wcag_reference": "1.4.1",
            "impact": "Los usuarios que no perciben bien los colores pueden no notar que estos elementos son interactivos.",
            "page_url": page_url,
            "affected_elements": [str(element) for element in problematic_elements]  # Lista de elementos afectados
        })

    return incidencias
