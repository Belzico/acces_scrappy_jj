from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_tab_aria_selected(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if the selected state of a tab with role="tab" is properly announced using aria-selected="true".
    
    - Finds elements with `role="tab"`.
    - Checks if at least one of them has `aria-selected="true"`.
    - If no tab is marked as selected, an issue is reported.

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL of the analyzed page.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    # 1) Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Find all elements with role="tab"
    tabs = soup.find_all(attrs={"role": "tab"})

    if not tabs:
        return []  # No tabs found, no issue detected

    selected_tab_found = any(tab.get("aria-selected") == "true" for tab in tabs)

    # 3) If no tab has aria-selected="true", generate an issue
    incidences = []
    if not selected_tab_found:
        incidences.append({
            "title": "Selected tab state is not announced",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": (
                "None of the tabs on the page have the attribute `aria-selected=\"true\"`. "
                "This means that screen reader users will not be able to identify which tab is active."
            ),
            "remediation": (
                "Add `aria-selected=\"true\"` to the active tab within a `role=\"tablist\"`. "
                "Example: `<button role=\"tab\" aria-selected=\"true\">My Groupons</button>`."
            ),
            "wcag_reference": "4.1.2",
            "impact": "Screen reader users may not know which tab is currently selected.",
            "page_url": page_url,
            "resolution": "check_tab_aria_selected.md"
        })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
