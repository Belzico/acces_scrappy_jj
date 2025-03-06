from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_mobile_button_aria_expanded(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if expandable buttons have `aria-expanded` properly set.

    - Finds buttons (`<button>`, elements with `role="button"`, or any element with `aria-expanded`).
    - Verifies if they have `aria-expanded="true"` or `aria-expanded="false"`.
    - If `aria-expanded` is missing, an issue is reported.

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL of the analyzed page.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    # 1) Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Find expandable control buttons
    expandable_buttons = []

    # a) Standard <button> elements
    expandable_buttons += soup.find_all("button")

    # b) Elements with role="button"
    expandable_buttons += soup.find_all(attrs={"role": "button"})

    # c) Any other element that has aria-expanded (for non-conventional structures)
    expandable_buttons += soup.find_all(attrs={"aria-expanded": True})

    if not expandable_buttons:
        return []  # No expandable buttons found, no issue detected

    incorrect_buttons = [
        btn for btn in expandable_buttons if btn.get("aria-expanded") not in ["true", "false"]
    ]

    # 3) If buttons without aria-expanded exist, generate an issue
    incidences = []
    if incorrect_buttons:
        incidences.append({
            "title": "Button has no expanded/collapsed state announced on mobile",
            "type": "Screen Readers",
            "severity": "Medium",
            "description": (
                "One or more expandable buttons are missing the `aria-expanded` attribute. "
                "This means that screen reader users on mobile devices "
                "will not know whether the button is expanded or collapsed."
            ),
            "remediation": (
                "Add `aria-expanded=\"true\"` or `aria-expanded=\"false\"` to the expandable button. "
                "Example: `<button aria-expanded=\"false\">See more</button>`."
            ),
            "wcag_reference": "4.1.2",
            "impact": "Screen reader users on mobile devices will not receive information about the button's state.",
            "page_url": page_url,
            "resolution": "check_mobile_button_aria_expanded.md"
        })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
