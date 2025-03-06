from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_zoom_text_cutoff(html_content, page_url, excel="issue_report.xlsx"):
    """
    Detects if text is cut off when zoomed to 200%.

    🔹 Checks for `overflow: hidden`, `height`, `max-height` in inline CSS.
    🔹 Identifies problematic classes like `hidden`, `truncate`, `text-cutoff`.
    🔹 Based on WCAG 1.4.4: Resize Text (https://www.w3.org/WAI/WCAG21/Understanding/resize-text.html).

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL of the analyzed page.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 1) Detect inline styles that may cause text cut-off
    problem_elements = []
    for tag in soup.find_all(style=True):
        style = tag["style"].lower()
        if "overflow: hidden" in style or "height:" in style or "max-height:" in style:
            problem_elements.append(tag)

    if problem_elements:
        incidences.append({
            "title": "Text may be cut off at 200% zoom",
            "type": "Zoom",
            "severity": "High",
            "description": (
                "Elements with `overflow: hidden;`, `height`, or `max-height` detected, which may "
                "cause content to be hidden when zoomed to 200%."
            ),
            "remediation": (
                "Ensure that containers can dynamically expand when text size increases. "
                "Avoid `overflow: hidden;` in critical content sections and use `min-height` instead of `height`."
            ),
            "wcag_reference": "1.4.4",
            "impact": "Users may lose access to important information when zooming.",
            "page_url": page_url,
            "resolution": "check_zoom_text_cutoff.md"
        })

    # 🔍 2) Detect common classes that may truncate text
    problematic_classes = {"hidden", "truncate", "text-cutoff", "text-hidden"}
    for tag in soup.find_all(class_=True):
        classes = set(tag["class"])
        if classes & problematic_classes:
            incidences.append({
                "title": "Text truncation detected",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    f"Classes `{classes & problematic_classes}` detected, which may truncate text "
                    "and prevent visibility when zoomed to 200%."
                ),
                "remediation": (
                    "Ensure that full content remains visible and accessible without requiring horizontal scrolling."
                ),
                "wcag_reference": "1.4.4",
                "impact": "Text may be hidden without a way for users to access it.",
                "page_url": page_url,
                "resolution": "check_zoom_text_cutoff.md"
            })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
