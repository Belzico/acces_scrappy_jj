from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_name_role_value(html_content, page_url,excel="issue_report.xlsx"):
    """
    Analyzes the HTML for UI components missing accessible name, role, or value.
    Based on WCAG 4.1.2 (Name, Role, Value, Level A).

    Parameters:
    - html_content (str): HTML code of the page.
    - page_url (str): URL or file path of the analyzed document.

    Returns:
    - List of detected issues.
    """

    soup = BeautifulSoup(html_content, 'html.parser')
    incidences = []

    # Find interactive elements without proper accessibility attributes
    interactive_elements = soup.find_all(["button", "input", "textarea", "select", "a", "div", "span"])

    for element in interactive_elements:
        element_id = element.get("id") or element.get("name") or "element without ID"
        element_info = {"tag": element.name, "id": element_id}

        # 1️⃣ Check if it has an accessible name
        has_name = element.get_text(strip=True) or element.get("aria-label") or element.get("aria-labelledby")
        if not has_name:
            incidences.append({
                "title": "Missing accessible name",
                "type": "Name, Role, Value",
                "severity": "High",
                "description": f"The element '{element.name}' with ID '{element_id}' does not have an accessible name.",
                "remediation": "Add an 'aria-label', 'aria-labelledby', or provide textual content.",
                "wcag_reference": "4.1.2",
                "impact": "Screen reader users may not understand the purpose of this element.",
                "page_url": page_url,
                "resolution": "check_name_role_value.md",
                "element_info": element_info
            })

        # 2️⃣ Check if it has a defined role when necessary
        if element.name in ["div", "span"] and not element.get("role"):
            incidences.append({
                "title": "Missing accessible role",
                "type": "Name, Role, Value",
                "severity": "Medium",
                "description": f"The element '{element.name}' with ID '{element_id}' does not have a defined role.",
                "remediation": "Add an appropriate 'role' attribute (e.g., role='button').",
                "wcag_reference": "4.1.2",
                "impact": "Assistive technologies may not recognize the intended function of this element.",
                "page_url": page_url,
                "resolution": "check_name_role_value.md",
                "element_info": element_info
            })

        # 3️⃣ Check if it has a programmatically determined state/value
        if element.name == "input" and element.get("type") in ["checkbox", "radio"]:
            if "aria-checked" not in element.attrs and "checked" not in element.attrs:
                incidences.append({
                    "title": "Missing programmatic value",
                    "type": "Name, Role, Value",
                    "severity": "High",
                    "description": f"The checkbox/radio '{element_id}' does not have a programmatically determined state.",
                    "remediation": "Add 'aria-checked' to indicate the state of the checkbox/radio.",
                    "wcag_reference": "4.1.2",
                    "impact": "Users relying on assistive technologies may not know the selected state.",
                    "page_url": page_url,
                    "resolution": "check_name_role_value.md",
                    "element_info": element_info
                })

    #Convertimos las incidencias directamente a Excel antes de retornar**
    transform_json_to_excel(incidences, excel)
    
    return incidences
