from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    return {
        "tag": element.name,
        "attrs": dict(element.attrs),
        "snippet": str(element)[:300]
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Check if there is a time limit (e.g., via meta refresh or script).\n"
            "3. Verify if there are controls/options to turn off, adjust, or extend the time limit."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("snippet", "")
    }

def run_all___2_2_1(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Busca meta refresh que imponga un límite de tiempo
    meta_refresh_tags = soup.find_all(
        "meta",
        attrs={"http-equiv": lambda x: x and x.lower() == "refresh"}
    )

    # Definimos palabras clave para un posible control que permita
    # desactivar, extender o ajustar el límite de tiempo
    keywords_for_controls = ["disable", "turn off", "extend", "adjust", "alargar", "desactivar", "extender"]

    for elem in meta_refresh_tags:
        content_attr = elem.get("content", "").lower()

        # Comprobamos si la meta refresh realmente apunta a una URL con tiempo
        # (p. ej. content="10; url=http://example.com")
        # En caso de que el content contenga algo como "10;" interpretamos que es un tiempo
        if ";" in content_attr or "url=" in content_attr:
            # Verifica si hay algún "control" para deshabilitar, ampliar o ajustar el tiempo
            has_control = soup.find(
                lambda t: (
                    t.name in ["button", "a"] and
                    any(keyword in t.get_text(strip=True).lower() for keyword in keywords_for_controls)
                )
            )

            if not has_control:
                raw_incidences.append({
                    "title": "Time limit enforced without user control",
                    "type": "Time-limits / Timeout",
                    "severity": "High",
                    "expected_result": (
                        "Any time limit should provide a mechanism to turn off, adjust, or extend it."
                    ),
                    "actual_result": (
                        f"Found a time limit via meta refresh ({elem}) without a visible control to disable or extend."
                    ),
                    "remediation": (
                        "Provide a mechanism (button, link, modal) that allows the user to disable, extend, "
                        "or otherwise adjust the time limit."
                    ),
                    "wcag_reference": "2.2.1",
                    "impact": (
                        "Users who need more time (e.g., due to cognitive or motor disabilities) may be "
                        "unable to complete tasks before timeout."
                    ),
                    "page_url": page_url,
                    "element_info": get_element_info(elem)
                })

    # Formatea las incidencias
    formatted = [format_incidence(i) for i in raw_incidences]

    # Si no hay incidencias, se añade una fila de justificación
    if not formatted:
        formatted.append({
            "Title": "Justificación de los CPs asignados que no generen issues",
            "Steps": "N/A",
            "Bug Type": "N/A",
            "Priority": "N/A",
            "Expected Result": "N/A",
            "Actual Result": "N/A",
            "Suggested resolution(s)": "N/A",
            "Failed checkpoint": "2.2.1",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    # Exporta los resultados a Excel
    transform_json_to_excel(formatted, excel)
    return formatted
