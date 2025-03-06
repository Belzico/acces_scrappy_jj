from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_button_aria_pressed(html_content, page_url, excel="issue_report.xlsx"):
    """
    Verifies if the selected state of a button with `role="button"` is correctly announced using `aria-pressed="true"`.
    
    - Finds elements with `role="button"`.
    - Checks if at least one has `aria-pressed="true"`.
    - If no button is marked as selected, an issue is reported.
    """

    # 1️⃣ Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2️⃣ Find all elements with role="button"
    buttons = soup.find_all(attrs={"role": "button"})

    if not buttons:
        return []  # No buttons with role="button", no issue generated

    selected_button_found = any(button.get("aria-pressed") == "true" for button in buttons)

    # 3️⃣ If no button has aria-pressed="true", generate an issue
    incidences = []
    if not selected_button_found:
        incidences.append({
            "title": "Selected button state is not announced",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": "No buttons on the page have the `aria-pressed=\"true\"` attribute. "
                           "This means screen reader users will not know which button is currently selected.",
            "remediation": "Ensure that the selected button includes `aria-pressed=\"true\"`. "
                           "Example: `<button role=\"button\" aria-pressed=\"true\">Global Position</button>`.",
            "wcag_reference": "4.1.2",
            "impact": "Screen reader users may not be aware of which button is selected.",
            "page_url": page_url,
            "resolution": "check_button_aria_pressed.md",
            "element_info": [str(btn) for btn in buttons]  # List of affected buttons
        })

    # Convert incidences to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
