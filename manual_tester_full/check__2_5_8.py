from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    return {
        "tag": element.name,
        "attrs": dict(element.attrs),
        "snippet": str(element)[:300]
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Identify the interactive element and measure its size and spacing.\n"
            "3. Check if it meets the 24x24 CSS pixels minimum or the spacing exception.\n"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("snippet", "")
    }

def run_all___2_5_8(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    INTERACTIVE_TAGS = ["button", "a", "input", "label", "textarea", "select"]
    for element in soup.find_all(INTERACTIVE_TAGS):
        style = element.get("style", "")
        width, height = None, None
        if "px" in style:
            for part in style.split(";"):
                if "width" in part:
                    try:
                        width = int(part.strip().split(":")[1].replace("px", "").strip())
                    except:
                        pass
                if "height" in part:
                    try:
                        height = int(part.strip().split(":")[1].replace("px", "").strip())
                    except:
                        pass

        if width is not None and height is not None and (width < 24 or height < 24):
            raw_incidences.append({
                "title": "Target smaller than 24x24 CSS pixels",
                "type": "Target Size (Minimum)",
                "severity": "Medium",
                "expected_result": (
                    "Interactive elements should be at least 24x24 CSS pixels, "
                    "or have sufficient spacing around them to avoid accidental activation."
                ),
                "actual_result": (
                    f"Element <{element.name}> has dimensions width: {width}px, height: {height}px."
                ),
                "remediation": (
                    "Increase the size of the target to 24x24 pixels or provide adequate spacing "
                    "(using 24px diameter spacing rule) from adjacent targets."
                ),
                "wcag_reference": "2.5.8",
                "impact": (
                    "Users with motor disabilities or touch input may struggle to activate small or tightly packed targets."
                ),
                "page_url": page_url,
                "element_info": get_element_info(element)
            })

    formatted = [format_incidence(i) for i in raw_incidences]

    if not formatted:
        formatted.append({
            "Title": "Justificación de los CPs asignados que no generen issues",
            "Steps": "N/A",
            "Bug Type": "N/A",
            "Priority": "N/A",
            "Expected Result": "N/A",
            "Actual Result": "N/A",
            "Suggested resolution(s)": "N/A",
            "Failed checkpoint": "2.5.8",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
