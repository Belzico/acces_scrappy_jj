from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  


def get_element_info(element):
    """
    Retrieves useful information about an HTML element to facilitate issue identification,
    and builds a unique Evidence field.
    """
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    # Construcción del campo "Evidence [SS or Video]"
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
    Transforms an incidence into the desired output format.
    'expected_result' and 'actual_result' must be clearly defined in each incidence.
    """
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {old.get('element_info', {}).get('tag', 'N/A')}\n"
            "3. Check the element’s visual styles and cues."
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("expected_result", "N/A"),
        "Actual Result": old.get("actual_result", "N/A"),
        "Suggested resolution(s)": old.get("Suggested resolution(s)"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact", "N/A"),
        "Evidence [SS or Video]": old.get("element_info", {}).get("evidence", "N/A")
    }


def run_all___1_4_1(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 🔹 CHECK 1: Buttons/Links that rely only on color
    elements = soup.find_all(["button", "a"])
    for element in elements:
        style = element.get("style", "").lower()
        uses_only_color = (
            "text-decoration: underline" not in style and
            "border" not in style and
            "background-color" not in style
        )
        if uses_only_color:
            raw_incidences.append({
                "title": "Buttons/links rely only on color",
                "type": "Color",
                "severity": "Low",
                "expected_result": (
                    "Interactive elements should provide additional visual cues "
                    "(underline, border, or background contrast) to indicate interactivity."
                ),
                "actual_result": (
                    "The button/link is identified only by color and lacks underline, "
                    "border, or background color."
                ),
                "Suggested resolution(s)": (
                    "Add visual cues such as text-decoration: underline for links, "
                    "border for buttons, or bold text to differentiate them from normal content."
                ),
                "wcag_reference": "1.4.1",
                "impact": (
                    "Users with color perception issues may not realize these elements are interactive."
                ),
                "page_url": page_url,
                "resolution": "check_buttons_only_by_color.md",
                "element_info": get_element_info(element)
            })

    formatted_incidences = [format_incidence(inc) for inc in raw_incidences]
    transform_json_to_excel(formatted_incidences, excel)
    return formatted_incidences
