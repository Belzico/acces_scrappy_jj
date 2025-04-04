from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_html_lines(html_content):
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    return "\n".join(f"{i+1}: {snippet[i - start]}" for i in range(start, end))

def get_element_info(element, html_lines=None):
    if element is None:
        return {
            "tag": "N/A",
            "text": "N/A",
            "line_number": "N/A",
            "evidence": "N/A",
            "fragment_html": "No <title> tag found in <head>."
        }

    tag = element.name if hasattr(element, 'name') else 'N/A'
    text = element.get_text(strip=True)[:50] if hasattr(element, 'get_text') else 'N/A'
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"
    evidence = f"<{tag}> at line {line_number}" if line_number != "N/A" else f"<{tag}>"

    snippet = ""
    if line_number != "N/A" and html_lines:
        try:
            snippet = get_line_snippet(html_lines, int(line_number))
        except Exception:
            pass

    return {
        "tag": tag,
        "text": text,
        "line_number": line_number,
        "evidence": evidence,
        "fragment_html": snippet
    }

def format_incidence(inc):
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the <title> element in the <head>.\n"
            f"3. Verify it exists and describes the page purpose.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n{snippet}"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": element_info.get("evidence", "N/A")
    }

def run_all___2_4_2(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
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
            "element_info": get_element_info(title_tag if title_tag else soup.html, html_lines=lines)
        }))

    if incidences:
        transform_json_to_excel(incidences, excel)

    return incidences
