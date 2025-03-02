from bs4 import BeautifulSoup

def check_mobile_button_aria_expanded(html_content, page_url):
    """
    Verifica si los botones con estados expandibles tienen `aria-expanded` correctamente configurado.
    
    - Busca botones (`<button>`, elementos con `role="button"`, o cualquier otro con `aria-expanded`).
    - Verifica si tienen `aria-expanded="true"` o `aria-expanded="false"`.
    - Si falta `aria-expanded`, se genera una incidencia.
    """

    # 1) Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Buscar botones de control expandible
    expandable_buttons = []

    # a) Botones estándar <button>
    expandable_buttons += soup.find_all("button")

    # b) Elementos con role="button"
    expandable_buttons += soup.find_all(attrs={"role": "button"})

    # c) Cualquier otro elemento que tenga aria-expanded (en caso de estructuras poco convencionales)
    expandable_buttons += soup.find_all(attrs={"aria-expanded": True})

    if not expandable_buttons:
        return []  # No hay botones con estados expandibles, no se genera incidencia

    incorrect_buttons = [
        btn for btn in expandable_buttons if btn.get("aria-expanded") not in ["true", "false"]
    ]

    # 3) Si hay botones sin aria-expanded, generamos incidencia
    incidencias = []
    if incorrect_buttons:
        incidencias.append({
            "title": "Button has no expanded/collapsed state announced on mobile",
            "type": "Screen Readers",
            "severity": "Medium",
            "description": (
                "Uno o más botones con estados expandibles no tienen el atributo `aria-expanded`. "
                "Esto significa que los usuarios con lectores de pantalla en dispositivos móviles "
                "no sabrán si el botón está expandido o colapsado."
            ),
            "remediation": (
                "Añadir `aria-expanded=\"true\"` o `aria-expanded=\"false\"` al botón expandible. "
                "Ejemplo: `<button aria-expanded=\"false\">Ver más</button>`."
            ),
            "wcag_reference": "4.1.2",
            "impact": "Los usuarios con lectores de pantalla en dispositivos móviles no recibirán información sobre el estado del botón.",
            "page_url": page_url,
        })

    return incidencias
