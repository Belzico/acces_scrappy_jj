from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

SKIP_TEXT_KEYWORDS = [
    "skip", "bypass", "omitir", "ir al contenido", 
    "saltar al contenido", "omitir menú", "omitir menu"
]
SKIP_HREF_TARGETS = [
    "#main", "#content", "#principal", "#maincontent", "#contenido"
]

def get_element_info(element):
    """
    Devuelve metadatos básicos del elemento (tag + primer texto).
    """
    return {
        "tag": element.name,
        "text": element.get_text(strip=True),
        "evidence": str(element)[:300]
    }

def format_incidence(inc):
    """
    Prepara el dict con el formato de columnas para exportar a Excel.
    """
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Check if there's a mechanism (skip link, main landmark, etc.) "
            "to bypass repeated blocks."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "")
    }

def run_all___2_4_1(html_content, page_url, excel="issue_report.xlsx"):
    """
    1. Parsea el contenido HTML.
    2. Comprueba si hay un skip link o un <main>/role="main">.
    3. Si no se encuentra nada, reporta error.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 1) Verificar si hay un elemento <main> o algo con role="main"
    has_main_landmark = bool(soup.find("main")) or bool(soup.find(attrs={"role": "main"}))

    # 2) Verificar si hay un skip link
    #    Criterios:
    #      - <a> con href que empiece en '#' (ancla interna)
    #      - texto contenga skip keywords
    #      - o href sea uno de los targets típicos (#main, #content, etc.)
    skip_link_found = False
    for link in soup.find_all("a"):
        href = link.get("href", "").lower()
        text = link.get_text(strip=True).lower()

        # Chequeo de href
        if href.startswith("#") and any(skipt in href for skipt in ["main", "content", "principal"]):
            skip_link_found = True
            break
        if any(kw in text for kw in SKIP_TEXT_KEYWORDS):
            skip_link_found = True
            break
        if href in SKIP_HREF_TARGETS:
            skip_link_found = True
            break

    # 3) Si ni skip link ni main => generamos incidencia
    if not has_main_landmark and not skip_link_found:
        raw_incidences.append({
            "title": "No mechanism to bypass repeated blocks",
            "type": "Navigation Aid",
            "severity": "High",
            "expected_result": "Provide a skip link or main landmark to quickly bypass repetitive content.",
            "actual_result": "Page lacks skip links or 'main' area to jump to.",
            "remediation": (
                "Add a <main> or role=\"main\", or include a skip link like "
                "<a href=\"#main-content\">Skip to main content</a>."
            ),
            "wcag_reference": "2.4.1",
            "impact": (
                "Keyboard or screen reader users must navigate through repeated content on every page."
            ),
            "page_url": page_url,
            "element_info": {
                "tag": "html",
                "text": "",
                "evidence": "No skip link or main landmark found."
            }
        })

    # 4) Generar la salida
    formatted = [format_incidence(i) for i in raw_incidences]

    # Si no hubo incidencias, agregamos fila de justificación
    if not formatted:
        formatted.append({
            "Title": "Justificación de los CPs asignados que no generen issues",
            "Steps": "N/A",
            "Bug Type": "N/A",
            "Priority": "N/A",
            "Expected Result": "N/A",
            "Actual Result": "N/A",
            "Suggested resolution(s)": "N/A",
            "Failed checkpoint": "2.4.1",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    # Exportar a Excel
    transform_json_to_excel(formatted, excel)
    return formatted
