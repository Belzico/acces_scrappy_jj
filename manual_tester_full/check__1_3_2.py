from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    """
    Devuelve información detallada del elemento HTML para el reporte,
    incluyendo una evidencia única y rastreable.
    """
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    evidence_parts = []
    if classes:
        evidence_parts.append(f"class={classes}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")

    evidence_str = ", ".join(evidence_parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_parts else tag

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }

def format_incidence(inc):
    """
    Estructura de salida estandarizada para el reporte de Excel.
    """
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the element: {inc.get('element_info', {}).get('tag', 'N/A')}.\n"
            f"3. Verify that the reading order is preserved and that re-positioning does not change meaning."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result", "N/A"),
        "Actual Result": inc.get("actual_result", "N/A"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact", "N/A"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "N/A")
    }

def run_all___1_3_2(html_content, page_url, excel="issue_report.xlsx"):
    """
    Verifica posibles errores de secuencias significativas (WCAG 1.3.2).
    Incluye:
      - Tablas que parezcan de maquetación (sin thead, th, caption, ni role='presentation')
      - Bloques con position:absolute en inline style (podría romper el orden lógico de lectura)
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 1) Detección de tablas "sospechosas" de ser layout
    tables = soup.find_all("table")
    for tbl in tables:
        # Buscamos <th>, <caption> o role="presentation" como indicadores de tabla semántica o tabla decorativa
        has_th = bool(tbl.find("th"))
        has_caption = bool(tbl.find("caption"))
        role_presentation = (tbl.get("role") == "presentation")

        if not (has_th or has_caption or role_presentation):
            info = get_element_info(tbl)
            raw_incidences.append({
                "title": "Possible layout table without semantic markers",
                "type": "Meaningful Sequence",
                "severity": "Medium",
                "expected_result": (
                    "Tables used for layout should be linearized or have role='presentation'. "
                    "Real data tables need <th> or <caption> for structure."
                ),
                "actual_result": (
                    "Found a <table> with no <th>, no <caption>, and no role='presentation'. "
                    "This may fail SC 1.3.2 if reflow changes the reading order."
                ),
                "remediation": (
                    "Use <th> / <caption> if it's a data table, or add role='presentation' "
                    "if purely for layout, ensuring reading order remains meaningful."
                ),
                "wcag_reference": "1.3.2",
                "impact": "Screen readers or reflows might present cells in a confusing order.",
                "page_url": page_url,
                "element_info": info
            })

    # 2) Detección de posicionamiento absoluto que podría indicar reordenamiento visual
    #    (F1: Failure if content meaning changes due to CSS positioning).
    absolutely_positioned = soup.find_all(style=re.compile(r"position\s*:\s*absolute", re.IGNORECASE))
    for element in absolutely_positioned:
        info = get_element_info(element)
        raw_incidences.append({
            "title": "Absolute positioning may alter reading sequence",
            "type": "Meaningful Sequence",
            "severity": "Low",
            "expected_result": "Ensure that absolute positioning does not break the logical reading order.",
            "actual_result": (
                "Element with position:absolute found. If content is visually moved away from its DOM position, "
                "it may confuse screen reader users."
            ),
            "remediation": (
                "Use CSS only to reorder content that doesn't affect meaning, or reorder the DOM to match the visual order."
            ),
            "wcag_reference": "1.3.2",
            "impact": "Users relying on screen readers may get content in the wrong order.",
            "page_url": page_url,
            "element_info": info
        })

    formatted = [format_incidence(inc) for inc in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)
    return formatted
