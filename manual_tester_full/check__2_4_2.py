from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],
        "line_number": element.sourceline if hasattr(element, "sourceline") else "N/A",
        "evidence": f"<{element.name}> at line {element.sourceline}" if hasattr(element, "sourceline") else f"<{element.name}>"
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the <title> element in the <head>.\n"
            f"3. Verify it exists and describes the page purpose."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "N/A")
    }

def run_all___2_4_2(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    incidences = []

    title_tag = soup.find("title")
    if not title_tag or not title_tag.get_text(strip=True):
        incidences.append(format_incidence({
            "title": "Missing or empty <title> element",
            "type": "Page Title",
            "severity": "High",
            "expected_result": "The page should have a non-empty <title> tag describing the topic or purpose.",
            "actual_result": "The page has no <title> element or it's empty.",
            "remediation": "Add a meaningful <title> element in the <head> of the page.",
            "wcag_reference": "2.4.2",
            "impact": "Users and assistive technologies cannot identify the page context.",
            "page_url": page_url,
            "element_info": get_element_info(title_tag if title_tag else soup.html)
        }))

    if incidences:
        transform_json_to_excel(incidences, excel)

    return incidences
