from bs4 import BeautifulSoup

def check_button_aria_pressed(html_content, page_url):
    """
    Verifica si el estado seleccionado de un botón con role="button" se anuncia correctamente con aria-pressed="true".
    
    - Busca elementos con `role="button"`.
    - Verifica si al menos uno tiene `aria-pressed="true"`.
    - Si no se encuentra ningún botón marcado como seleccionado, se genera una incidencia.
    """

    # 1) Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Buscar todos los elementos con role="button"
    buttons = soup.find_all(attrs={"role": "button"})

    if not buttons:
        return []  # No hay botones con role="button", no se genera incidencia

    selected_button_found = any(button.get("aria-pressed") == "true" for button in buttons)

    # 3) Si no hay ningún botón con aria-pressed="true", generamos incidencia
    incidencias = []
    if not selected_button_found:
        incidencias.append({
            "title": "Visually selected button is not announced",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": (
                "Ningún botón en la página tiene el atributo `aria-pressed=\"true\"`. "
                "Esto significa que los usuarios con lectores de pantalla no sabrán qué botón está seleccionado."
            ),
            "remediation": (
                "Añadir `aria-pressed=\"true\"` al botón seleccionado. "
                "Ejemplo: `<button role=\"button\" aria-pressed=\"true\">Posición Global</button>`."
            ),
            "wcag_reference": "4.1.2",
            "impact": "Los usuarios con lectores de pantalla podrían no saber cuál botón está seleccionado.",
            "page_url": page_url,
        })

    return incidencias
