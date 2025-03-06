from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def get_element_info(element):
    """Retrieves useful information about an HTML element to facilitate issue identification."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # First 50 characters of the text
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"
    }

def check_buttons_only_by_color(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if buttons and links rely only on color for identification.

    - Finds `<button>` and `<a>` elements in the page.
    - Verifies if they have visual cues like `text-decoration: underline`, `border`, or `background-color`.
    - If they rely only on color without additional visual indicators, an issue is reported.
    """

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all buttons and links
    elements = soup.find_all(["button", "a"])

    # Identify elements that rely only on color
    problematic_elements = []
    for element in elements:
        style = element.get("style", "").lower()

        # Conditions to check if the element uses only color
        uses_only_color = (
            "text-decoration: underline" not in style and
            "border" not in style and
            "background-color" not in style
        )

        # Add to the list if it relies only on color
        if uses_only_color:
            problematic_elements.append(element)

    incidences = []
    for element in problematic_elements:
        incidences.append({
            "title": "Buttons/links rely only on color",
            "type": "Color",
            "severity": "Low",
            "description": "Some buttons or links are identified only by color without additional visual cues. "
                           "Users with visual impairments may not recognize them correctly.",
            "remediation": "Add visual cues such as `text-decoration: underline` for links, `border` for buttons, "
                           "or bold text to differentiate them from normal content.",
            "wcag_reference": "1.4.1",
            "impact": "Users with color perception issues may not realize these elements are interactive.",
            "page_url": page_url,
            "resolution": "check_buttons_only_by_color.md",
            "element_info": get_element_info(element)
        })

    # Convert incidences to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
