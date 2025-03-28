from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel

# Función para calcular la luminancia relativa de un color
def luminance(color):
    r, g, b = [int(color[i:i+2], 16) / 255.0 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return (0.2126 * rgb[0]) + (0.7152 * rgb[1]) + (0.0722 * rgb[2])

# Función para calcular la relación de contraste entre dos colores
def contrast_ratio(color1, color2):
    lum1, lum2 = luminance(color1), luminance(color2)
    return (max(lum1, lum2) + 0.05) / (min(lum1, lum2) + 0.05)

def get_element_info(element):
    """
    Devuelve información detallada del elemento HTML para el reporte,
    incluyendo una evidencia única y rastreable.
    """
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
    """
    Formatea una incidencia para incluir evidencia visual y pasos detallados.
    """
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {old.get('element_info', {}).get('tag', 'N/A')}\n"
            f"3. Review the contrast settings in style attributes."
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

def check_dropdown_contrast(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    dropdowns = soup.find_all("select")
    incidences = []

    for dropdown in dropdowns:
        selected_option = dropdown.find("option", selected=True) or dropdown.find("option")
        if selected_option:
            text_color_match = re.search(r'color:\s*(#[0-9A-Fa-f]{6})', selected_option.get("style", ""))
            bg_color_match = re.search(r'background-color:\s*(#[0-9A-Fa-f]{6})', selected_option.get("style", ""))
            text_color = text_color_match.group(1) if text_color_match else "#000000"
            bg_color = bg_color_match.group(1) if bg_color_match else "#FFFFFF"
            contrast = contrast_ratio(text_color, bg_color)

            if contrast < 4.5:
                incidences.append({
                    "title": "Dropdown selected value fails contrast once expanded",
                    "type": "Color Contrast",
                    "severity": "High",
                    "expected_result": "The selected dropdown option should have a contrast ratio of at least 4.5:1 between text and background.",
                    "actual_result": f"The selected dropdown option has a contrast ratio of {contrast:.2f}:1.",
                    "remediation": (
                        "Use a darker text color or change the background to increase contrast. "
                        "Example: `color: #2C3E50;` instead of a lighter color."
                    ),
                    "wcag_reference": "1.4.3",
                    "impact": "Users with low vision may not be able to read the selected dropdown text.",
                    "page_url": page_url,
                    "element_info": get_element_info(selected_option)
                })
    return incidences

def check_placeholder_contrast(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    inputs = soup.find_all("input", attrs={"placeholder": True})
    incidences = []

    for input_field in inputs:
        text_color_match = re.search(r'color:\s*(#[0-9A-Fa-f]{6})', input_field.get("style", ""))
        bg_color_match = re.search(r'background-color:\s*(#[0-9A-Fa-f]{6})', input_field.get("style", ""))
        text_color = text_color_match.group(1) if text_color_match else "#BFCAD1"
        bg_color = bg_color_match.group(1) if bg_color_match else "#FFFFFF"
        contrast = contrast_ratio(text_color, bg_color)

        if contrast < 4.5:
            incidences.append({
                "title": "Grey placeholder fails contrast on white background",
                "type": "Color Contrast",
                "severity": "High",
                "expected_result": "The placeholder text should have a contrast ratio of at least 4.5:1 against the background.",
                "actual_result": f"The placeholder text has a contrast ratio of {contrast:.2f}:1.",
                "remediation": (
                    "Use a darker color for the placeholder text or change the background to improve contrast. "
                    "Example: `color: #757575;` instead of `color: #BFCAD1;`."
                ),
                "wcag_reference": "1.4.3",
                "impact": "Users with low vision may struggle to read the placeholder text.",
                "page_url": page_url,
                "element_info": get_element_info(input_field)
            })
    return incidences

def run_all___1_4_3(html_content, page_url, excel="issue_report.xlsx"):
    incidences = []
    incidences += check_dropdown_contrast(html_content, page_url)
    incidences += check_placeholder_contrast(html_content, page_url)

    formatted_incidences = [format_incidence(inc) for inc in incidences]
    if formatted_incidences:
        transform_json_to_excel(formatted_incidences, excel)

    return formatted_incidences
