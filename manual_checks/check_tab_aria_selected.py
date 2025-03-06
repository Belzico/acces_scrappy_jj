from bs4 import BeautifulSoup

def check_tab_aria_selected(html_content, page_url):
    """
    Verifica si el estado seleccionado de una pestaña con role="tab" se anuncia correctamente con aria-selected="true".
    
    - Busca elementos con `role="tab"`.
    - Verifica si al menos uno de ellos tiene `aria-selected="true"`.
    - Si no se encuentra ninguna pestaña marcada como seleccionada, se genera una incidencia.
    """

    # 1) Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Buscar todos los elementos con role="tab"
    tabs = soup.find_all(attrs={"role": "tab"})

    if not tabs:
        return []  # No hay pestañas, no hay incidencia

    selected_tab_found = any(tab.get("aria-selected") == "true" for tab in tabs)

    # 3) Si no hay ninguna pestaña con aria-selected="true", generamos incidencia
    incidencias = []
    if not selected_tab_found:
        incidencias.append({
            "title": "Selected tab state is not announced",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": (
                "Ninguna de las pestañas en la página tiene el atributo `aria-selected=\"true\"`. "
                "Esto significa que los usuarios con lectores de pantalla no sabrán cuál pestaña está activa."
            ),
            "remediation": (
                "Añadir `aria-selected=\"true\"` a la pestaña activa dentro de un `role=\"tablist\"`. "
                "Ejemplo: `<button role=\"tab\" aria-selected=\"true\">My Groupons</button>`."
            ),
            "wcag_reference": "4.1.2",
            "impact": "Los usuarios con lectores de pantalla podrían no saber cuál pestaña está seleccionada.",
            "page_url": page_url,
        })

    return incidencias
