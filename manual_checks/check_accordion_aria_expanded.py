from bs4 import BeautifulSoup

def check_accordion_aria_expanded(html_content, page_url):
    """
    Verifica si los botones de acordeón tienen el atributo aria-expanded correctamente configurado.
    
    - Busca todos los acordeones (botones con `aria-expanded` o `role="button"`).
    - Si algún botón no tiene `aria-expanded="true"` o `aria-expanded="false"`, se genera una incidencia.
    """

    # 1) Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Buscar todos los posibles botones de acordeón
    accordion_buttons = soup.find_all("button", class_="accordion-toggle")  # Botones estándar
    accordion_buttons += soup.find_all(attrs={"role": "button", "class": "accordion-toggle"})  # Elementos con role="button"
    accordion_buttons += soup.find_all("a", class_="accordion-toggle")  # Opcionalmente, enlaces

    if not accordion_buttons:
        return []  # No hay acordeones, no se genera incidencia

    incorrect_buttons = [
        btn for btn in accordion_buttons if btn.get("aria-expanded") not in ["true", "false"]
    ]

    # 3) Si hay botones sin aria-expanded, generamos incidencia
    incidencias = []
    if incorrect_buttons:
        incidencias.append({
            "title": "Accordion items don’t announce state",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": (
                "Uno o más botones de acordeón no tienen el atributo `aria-expanded`. "
                "Esto significa que los usuarios con lectores de pantalla no sabrán si el acordeón está expandido o colapsado."
            ),
            "remediation": (
                "Añadir `aria-expanded=\"true\"` o `aria-expanded=\"false\"` al botón de acordeón. "
                "Ejemplo: `<button aria-expanded=\"false\">Sección 1</button>`."
            ),
            "wcag_reference": "4.1.2",
            "impact": "Los usuarios con lectores de pantalla podrían no saber que hay contenido expandible en la página.",
            "page_url": page_url,
        })

    return incidencias
