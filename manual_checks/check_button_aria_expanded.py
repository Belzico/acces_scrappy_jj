from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_button_aria_expanded(html_content, page_url, excel="issue_report.xlsx"):
    """
    Verifica si los botones con estados expandibles tienen `aria-expanded` correctamente configurado.
    
    - Busca botones (`<button>` o elementos con `role="button"`).
    - Verifica si tienen `aria-expanded="true"` o `aria-expanded="false"`.
    - Si falta `aria-expanded`, se genera una incidencia.
    """

    # 1️⃣ Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2️⃣ Buscar botones de control expandible
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

    # 3️⃣ Si hay botones sin aria-expanded, generamos incidencias
    incidences = []
    for btn in incorrect_buttons:
        incidences.append({
            "title": "Expandable button missing aria-expanded",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": "One or more expandable buttons do not have the `aria-expanded` attribute. "
                           "This means screen reader users will not know whether the button is expanded or collapsed.",
            "remediation": "Ensure that expandable buttons include `aria-expanded=\"true\"` or `aria-expanded=\"false\"`. "
                           "Example: `<button aria-expanded=\"false\">Categories</button>`.",
            "wcag_reference": "4.1.2",
            "impact": "Screen reader users may not receive correct information about the button state.",
            "page_url": page_url,
            "element_info": [str(btn)]  # Lista los botones con errores
        })

    # Convertir incidencias a Excel antes de retornar
    transform_json_to_excel(incidences, excel)

    return incidences
