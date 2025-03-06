from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel  

def check_reflow_320px(html_content, page_url, excel="issue_report.xlsx"):
    """
    Detects reflow issues when the page is viewed at 320px width.

    🔹 Identifies elements with fixed widths that may cause overflow.
    🔹 Checks for forced horizontal scrolling.
    🔹 Analyzes inline and embedded CSS styles.
    🔹 Based on WCAG 1.4.10: Reflow (https://www.w3.org/WAI/WCAG21/Understanding/reflow.html).

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL (or identifier) of the analyzed page.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 1) Detect elements with fixed width in inline styles (`style="width: 600px;"`)
    problem_elements = []
    for tag in soup.find_all(style=True):
        style = tag["style"].lower()
        if re.search(r"width:\s*\d+px", style) and "max-width" not in style:
            problem_elements.append(tag)

    if problem_elements:
        incidences.append({
            "title": "Fixed width elements detected (inline styles)",
            "type": "Zoom",
            "severity": "High",
            "description": (
                "Elements with fixed pixel widths were found in `style` attributes, "
                "which may prevent content from adapting properly to a 320px viewport."
            ),
            "remediation": (
                "Replace fixed widths (`width: 600px;`) with flexible values (`max-width: 100%`, `flexbox`, `grid`)."
            ),
            "wcag_reference": "1.4.10",
            "impact": "Users must scroll horizontally to view content, making navigation difficult.",
            "page_url": page_url,
            "resolution": "check_reflow_320px.md"
        })

    # 🔍 2) Check for fixed width in embedded CSS within <style> tags
    css_rules = []
    for style_tag in soup.find_all("style"):
        css_rules.extend(style_tag.get_text().split(";"))

    for rule in css_rules:
        if re.search(r"width:\s*\d+px", rule) and "max-width" not in rule:
            incidences.append({
                "title": "Fixed width detected in CSS",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    "A `width: Xpx` was detected in the page's CSS styles without `max-width`, "
                    "which may prevent content from adapting properly to a 320px viewport."
                ),
                "remediation": (
                    "Avoid `width: Xpx;` and use `max-width: 100%` or flexible CSS with `grid` or `flexbox`."
                ),
                "wcag_reference": "1.4.10",
                "impact": "Users cannot view content without horizontal scrolling, which is a poor mobile practice.",
                "page_url": page_url,
                "resolution": "check_reflow_320px.md"
            })

    # 🔍 3) Check if forced horizontal scrolling is present due to `overflow-x`
    for tag in soup.find_all(style=True):
        style = tag["style"].lower()
        if "overflow-x: auto" in style or "overflow-x: scroll" in style:
            incidences.append({
                "title": "Horizontal scrolling detected",
                "type": "Zoom",
                "severity": "High",
                "description": (
                    "A horizontal scrollbar was detected on the page, indicating that "
                    "the content does not properly adjust to a 320px viewport."
                ),
                "remediation": (
                    "Modify containers to use `max-width: 100%` and avoid `overflow-x: scroll`."
                ),
                "wcag_reference": "1.4.10",
                "impact": "Users cannot view content without horizontal scrolling, which is a poor mobile practice.",
                "page_url": page_url,
                "resolution": "check_reflow_320px.md"
            })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
