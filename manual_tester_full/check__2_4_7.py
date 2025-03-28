from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel


def get_element_info(element):
    """Devuelve información detallada del elemento HTML para el reporte,
    incluyendo una evidencia única y rastreable."""
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    evidence_parts = []
    if classes:
        evidence_parts.append(f"class={classes}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")

    evidence_str = ", ".join(evidence_parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_str else tag

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }


def format_incidence(old):
    """Convierte una incidencia raw al formato estandarizado para exportar a Excel."""
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {old.get('element_info', {}).get('tag', 'N/A')}\n"
            f"3. Press TAB repeatedly to check for visible focus indicators."
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("expected_result", "N/A"),
        "Actual Result": old.get("actual_result", "N/A"),
        "Suggested resolution(s)": old.get("remediation"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact", "N/A"),
        "Evidence [SS or Video]": old.get("element_info", {}).get("evidence", "N/A")
    }


def check_focus_visible(html_content, page_url):
    """
    Tester para WCAG 2.4.7 - Focus Visible.
    Detecta elementos sin indicador de foco visible o sin tabindex adecuado.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    focusable_elements = soup.find_all(["a", "button", "input", "select", "textarea", "iframe", "div", "span"])
    raw_incidences = []

    for element in focusable_elements:
        info = get_element_info(element)
        styles = element.get("style", "").lower()

        # 1️⃣ Ocultar el foco con CSS
        if "outline:none" in styles or "outline: 0" in styles or "border: none" in styles:
            raw_incidences.append({
                "title": "Element without visible focus indicator",
                "type": "Focus Visibility",
                "severity": "High",
                "expected_result": "The element should display a visible focus indicator when selected.",
                "actual_result": f"The element hides focus using styles: {styles}",
                "remediation": "Ensure focus is visible by adding `:focus` or `:focus-visible` in CSS.",
                "wcag_reference": "2.4.7",
                "impact": "Keyboard users cannot see which element is focused.",
                "page_url": page_url,
                "element_info": info
            })

        # 2️⃣ Elemento interactivo sin tabindex
        if element.name in ["div", "span"] and ("onclick" in element.attrs or "role" in element.attrs):
            if "tabindex" not in element.attrs:
                raw_incidences.append({
                    "title": "Interactive element without tabindex",
                    "type": "Focus Visibility",
                    "severity": "Medium",
                    "expected_result": "Interactive elements must be keyboard-focusable via `tabindex='0'`.",
                    "actual_result": f"The <{element.name}> element is interactive but lacks `tabindex`.",
                    "remediation": "Add `tabindex='0'` so it can receive keyboard focus.",
                    "wcag_reference": "2.4.7",
                    "impact": "Keyboard users cannot access this element.",
                    "page_url": page_url,
                    "element_info": info
                })

        # 3️⃣ tabindex=-1
        if "tabindex" in element.attrs and element.attrs["tabindex"] == "-1":
            raw_incidences.append({
                "title": "Element with tabindex='-1'",
                "type": "Focus Visibility",
                "severity": "Medium",
                "expected_result": "The element should be reachable via keyboard unless explicitly excluded.",
                "actual_result": "The element is removed from keyboard navigation via `tabindex='-1'`.",
                "remediation": "Avoid using `tabindex='-1'` unless an accessible alternative is provided.",
                "wcag_reference": "2.4.7",
                "impact": "The element will not be accessible via keyboard.",
                "page_url": page_url,
                "element_info": info
            })

        # 4️⃣ Elementos ocultos al recibir foco
        if "display:none" in styles or "visibility:hidden" in styles:
            raw_incidences.append({
                "title": "Element hidden when receiving focus",
                "type": "Focus Visibility",
                "severity": "High",
                "expected_result": "Elements should remain visible when focused.",
                "actual_result": f"The element is hidden via CSS: {styles}",
                "remediation": "Ensure the element remains visible when it receives focus.",
                "wcag_reference": "2.4.7",
                "impact": "Users may lose navigation context.",
                "page_url": page_url,
                "element_info": info
            })

    return raw_incidences


def run_all___2_4_7(html_content, page_url, excel="issue_report.xlsx"):
    """
    Método integrador para WCAG 2.4.7 - ejecuta check_focus_visible y exporta el resultado.
    """
    raw = check_focus_visible(html_content, page_url)
    formatted = [format_incidence(inc) for inc in raw]

    if formatted:
        transform_json_to_excel(formatted, excel)

    return formatted
