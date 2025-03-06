from bs4 import BeautifulSoup

def check_aria_label_in_div(html_content, page_url):
    """
    Verifica si existen `<div>` con `aria-label` sin un `role` definido.

    - Busca todos los `<div>` que tienen el atributo `aria-label`.
    - Verifica si tienen un `role` válido.
    - Si falta el `role`, genera una incidencia.
    """

    # 1) Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Buscar todos los <div> con aria-label
    divs_with_aria_label = soup.find_all("div", attrs={"aria-label": True})

    # 3) Filtrar los que no tienen un role definido
    invalid_divs = [div for div in divs_with_aria_label if not div.has_attr("role")]

    # 4) Generar incidencias si hay <div> con aria-label sin role
    incidencias = []
    if invalid_divs:
        incidencias.append({
            "title": "Aria-label attribute incorrectly used in div elements",
            "type": "HTML Validator",
            "severity": "Low",
            "description": (
                "El atributo `aria-label` solo debe usarse en elementos que lo soporten. "
                "Actualmente se encuentra en `<div>` sin un `role` definido, lo que no es válido."
            ),
            "remediation": (
                "Asegurar que los `<div>` con `aria-label` tengan un `role` apropiado, como `role=\"button\"`, `role=\"option\"`, etc. "
                "Si el `aria-label` no es necesario, usar un `<span>` o `<button>` en su lugar."
            ),
            "wcag_reference": "4.1.2",
            "impact": "No hay impacto inmediato, pero puede causar problemas en validadores y tecnologías asistivas.",
            "page_url": page_url,
            "affected_elements": [str(div) for div in invalid_divs]  # Lista los <div> con errores
        })

    return incidencias
