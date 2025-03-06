from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_menu_text_spacing(html_content, page_url, excel="issue_report.xlsx"):
    """
    Detects if menu items overflow or get cut off when text spacing adjustments are applied.

    🔹 Based on WCAG 1.4.12: Text Spacing.
    🔹 Identifies issues with `overflow: hidden;`, `white-space: nowrap;`, and `max-height` in menus.
    🔹 Checks if menu text overflows or becomes unreadable.

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL of the analyzed page.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 Find all navigation elements that may contain menus
    menus = soup.find_all(["nav", "ul", "div"], class_=["menu", "navigation", "navbar"])

    for menu in menus:
        # 🔍 Check styles that could cause spacing issues
        for item in menu.find_all(["li", "a", "span", "div"]):
            style = item.get("style", "").lower()

            if "overflow: hidden" in style:
                incidences.append({
                    "title": "Content may be cropped with text spacing adjustments",
                    "type": "Zoom",
                    "severity": "High",
                    "description": (
                        "`overflow: hidden;` was detected in a menu item. "
                        "This may cause content to be cut off when text spacing is increased."
                    ),
                    "remediation": (
                        "Avoid using `overflow: hidden;` in menu items. "
                        "Ensure that content expands properly."
                    ),
                    "wcag_reference": "1.4.12",
                    "impact": "Users who need additional spacing may not see the full content.",
                    "page_url": page_url,
                    "resolution": "check_menu_text_spacing.md"
                })

            if "white-space: nowrap" in style:
                incidences.append({
                    "title": "Text does not wrap in the menu",
                    "type": "Zoom",
                    "severity": "High",
                    "description": (
                        "`white-space: nowrap;` was detected, preventing text from wrapping properly "
                        "when text spacing is increased."
                    ),
                    "remediation": (
                        "Avoid using `white-space: nowrap;` in menus to allow text to adjust correctly."
                    ),
                    "wcag_reference": "1.4.12",
                    "impact": "Menu items may overflow from their container.",
                    "page_url": page_url,
                    "resolution": "check_menu_text_spacing.md"
                })

            if "max-height" in style and "px" in style:
                incidences.append({
                    "title": "Menu items may be cut off",
                    "type": "Zoom",
                    "severity": "High",
                    "description": (
                        "`max-height` in pixels was detected in a menu, which may cause items "
                        "to be cropped when text spacing increases."
                    ),
                    "remediation": (
                        "Use `min-height: auto;` instead of fixed values to allow dynamic adjustment."
                    ),
                    "wcag_reference": "1.4.12",
                    "impact": "Users may not see the full content of the menu.",
                    "page_url": page_url,
                    "resolution": "check_menu_text_spacing.md"
                })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
