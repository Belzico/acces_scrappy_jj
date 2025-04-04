from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

GENERIC_TERMS = {
    "heading", "title", "untitled", "label", "header", "section", "example heading",
    "my heading", "test heading", "my label", "test label", "form label"
}

def get_html_lines(html_content):
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    return "\n".join(f"{i+1}: {snippet[i - start]}" for i in range(start, end))

def get_element_info(element, html_lines=None):
    tag = element.name
    text = element.get_text(strip=True)
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

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
        "evidence": snippet or str(element)[:300]
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the <{inc.get('element_info', {}).get('tag')}> element with text: "
            f"\"{inc.get('element_info', {}).get('text')}\".\n"
            f"HTML snippet:\n{inc.get('element_info', {}).get('evidence', '')}"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "")
    }

def run_all___2_4_6(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []
    lines = get_html_lines(html_content)

    # Headings
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    for heading in headings:
        text = heading.get_text(strip=True).lower()
        if not text or text in GENERIC_TERMS:
            raw_incidences.append({
                "title": "Non-descriptive heading",
                "type": "Headings & Labels",
                "severity": "Medium",
                "expected_result": "Headings should clearly describe the content that follows.",
                "actual_result": f"Heading is empty or uses generic text: \"{text}\"",
                "remediation": (
                    "Replace with a concise, meaningful heading (e.g., 'About Our Services', 'Instructions')."
                ),
                "wcag_reference": "2.4.6",
                "impact": (
                    "Users with cognitive or visual disabilities may struggle to understand page structure."
                ),
                "page_url": page_url,
                "element_info": get_element_info(heading, lines)
            })

    # Labels
    labels = soup.find_all("label")
    for lbl in labels:
        text = lbl.get_text(strip=True).lower()
        if not text or text in GENERIC_TERMS:
            raw_incidences.append({
                "title": "Non-descriptive label",
                "type": "Headings & Labels",
                "severity": "Medium",
                "expected_result": "Labels should clearly indicate what input is requested.",
                "actual_result": f"Label is empty or uses generic text: \"{text}\"",
                "remediation": (
                    "Use descriptive text (e.g., 'First Name', 'Search Terms'). "
                    "If hidden visually, ensure the accessible name is still descriptive."
                ),
                "wcag_reference": "2.4.6",
                "impact": (
                    "Users relying on screen readers or with cognitive impairments may not understand the label."
                ),
                "page_url": page_url,
                "element_info": get_element_info(lbl, lines)
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
            "Failed checkpoint": "2.4.6",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
