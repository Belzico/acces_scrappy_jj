import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_text_spacing_cropping(html_content, page_url, excel="issue_report.xlsx"):
    """
    Detects if content is cropped when accessible text spacing rules are applied (WCAG 1.4.12).
    Checks containers with `overflow: hidden;` and fixed heights in inline styles.

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL of the analyzed page.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 1) Find elements (p, div, span, etc.) with inline styles
    text_containers = soup.find_all(["p", "div", "span", "section", "article"], style=True)

    # Regex to detect `overflow: hidden;`, `overflow-x: hidden;`, or `overflow-y: hidden;`
    overflow_hidden_regex = re.compile(r"overflow(?:-x|-y)?\s*:\s*hidden", re.IGNORECASE)

    # Regex to detect fixed `height` in pixels
    height_fixed_regex = re.compile(r"height\s*:\s*\d+px", re.IGNORECASE)

    for element in text_containers:
        style_attr = element["style"].lower()

        # 2) Detect `overflow: hidden;` (in all variants)
        if overflow_hidden_regex.search(style_attr):
            incidences.append({
                "title": "Content may be cropped with text spacing adjustments",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    "`overflow: hidden;` (or a variation -x/-y) was detected in a text container. "
                    "This may cause content to be cut off when text spacing is increased."
                ),
                "remediation": (
                    "Avoid using `overflow: hidden;` in text containers when applying additional spacing. "
                    "Use `overflow: visible;` or allow dynamic expansion."
                ),
                "wcag_reference": "1.4.12",
                "impact": "Users who need extra spacing may not see the full content.",
                "page_url": page_url,
                "resolution": "check_text_spacing_cropping.md"
            })

        # 3) Detect fixed height in pixels
        if height_fixed_regex.search(style_attr):
            incidences.append({
                "title": "Fixed height detected, may crop text",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    "A fixed height in pixels (`height: XXXpx;`) was detected in a text container. "
                    "This may prevent text from adjusting when extra spacing is applied."
                ),
                "remediation": (
                    "Use `min-height: auto;` instead of fixed heights to allow dynamic expansion."
                ),
                "wcag_reference": "1.4.12",
                "impact": "Text may be cut off when users increase spacing.",
                "page_url": page_url,
                "resolution": "check_text_spacing_cropping.md"
            })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
