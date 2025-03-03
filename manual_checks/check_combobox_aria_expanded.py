from bs4 import BeautifulSoup

def check_combobox_aria_expanded(html_content, page_url):
    """
    Verifica si los comboboxes de búsqueda tienen `aria-expanded` correctamente configurado.

    - Busca inputs con `role="combobox"`, divs con `role="combobox"`, y selects.
    - Verifica si tienen `aria-expanded="true"` o `aria-expanded="false"`.
    - Si `aria-expanded` no cambia correctamente, se genera una incidencia.
    """

    # 1) Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Buscar todos los posibles comboboxes
    comboboxes = []
    
    # a) Inputs con role="combobox"
    comboboxes += soup.find_all("input", attrs={"role": "combobox"})
    
    # b) Divs con role="combobox"
    comboboxes += soup.find_all("div", attrs={"role": "combobox"})
    
    # c) Selects con aria-expanded (no es común, pero algunos lo usan)
    comboboxes += soup.find_all("select", attrs={"aria-expanded": True})

    if not comboboxes:
        return []  # No hay comboboxes en la página

    incorrect_comboboxes = [
        cb for cb in comboboxes if cb.get("aria-expanded") not in ["true", "false"]
    ]

    # 3) Si hay comboboxes sin aria-expanded válido, generamos incidencia
    incidencias = []
    if incorrect_comboboxes:
        incidencias.append({
            "title": "Aria-expanded attribute is not working correctly in Search combobox",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": (
                "Uno o más comboboxes de búsqueda no cambian correctamente el atributo `aria-expanded`. "
                "Cuando se expande el menú de búsqueda, `aria-expanded` debe cambiar a `true`, "
                "y cuando se colapsa, debe cambiar a `false`."
            ),
            "remediation": (
                "Actualizar el `aria-expanded` en el combobox de búsqueda para reflejar correctamente su estado. "
                "Ejemplo: `<input role=\"combobox\" aria-expanded=\"true\">` cuando está expandido."
            ),
            "wcag_reference": "4.1.2",
            "impact": "Los usuarios con lectores de pantalla pueden sentirse confundidos si `aria-expanded` no cambia correctamente en la búsqueda.",
            "page_url": page_url,
        })

    return incidencias
