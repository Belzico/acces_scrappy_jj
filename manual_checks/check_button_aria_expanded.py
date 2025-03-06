from bs4 import BeautifulSoup

def check_button_aria_expanded(html_content, page_url):
    """
    Verifica si los botones con estados expandibles tienen `aria-expanded` correctamente configurado.
    
    - Busca botones (`<button>` o elementos con `role="button"`).
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

    # c) Cualquier otro elemento con aria-expanded (para estructuras atípicas)
    expandable_buttons += soup.find_all(attrs={"aria-expanded": True})

    if not expandable_buttons:
        return []  # No hay botones expandibles, no se genera incidencia

    incorrect_buttons = [
        btn for btn in expandable_buttons if btn.get("aria-expanded") not in ["true", "false"]
    ]

    # 3) Si hay botones sin aria-expanded, generamos incidencia
    incidencias = []
    if incorrect_buttons:
        incidencias.append({
            "title": "Expanded/Collapsed state is not announced in the button",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": (
                "Uno o más botones que expanden o colapsan contenido no tienen el atributo `aria-expanded`. "
                "Esto significa que los usuarios con lectores de pantalla no sabrán si el botón está expandido o colapsado."
            ),
            "remediation": (
                "Añadir `aria-expanded=\"true\"` o `aria-expanded=\"false\"` al botón expandible. "
                "Ejemplo: `<button aria-expanded=\"false\">Categories</button>`."
            ),
            "wcag_reference": "4.1.2",
            "impact": "Los usuarios con lectores de pantalla no recibirán información sobre el estado del botón.",
            "page_url": page_url,
        })

    return incidencias
