from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

AMBIGUOUS_LINK_TEXT = [
    "click here", "here", "more", "read more", "read more...", "learn more",
    "ver más", "hacer clic aquí", "pulsa aquí", "aquí", "ver más..."
]

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
        "evidence": str(element)[:300],
        "fragment_html": snippet
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the link with text: \"{inc.get('element_info', {}).get('text')}\".\n"
            f"HTML snippet (around line {inc.get('element_info', {}).get('line_number', 'N/A')}):\n"
            f"{inc.get('element_info', {}).get('fragment_html', '')}"
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

def run_all___2_4_4(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []
    lines = get_html_lines(html_content)

    all_links = soup.find_all("a")

    for link in all_links:
        link_text = link.get_text(strip=True)
        lower_text = link_text.lower()

        if not link_text:
            raw_incidences.append({
                "title": "Link text is empty",
                "type": "Link Purpose",
                "severity": "High",
                "expected_result": "Links must have accessible text indicating their purpose.",
                "actual_result": "Found a link (<a>) with no link text.",
                "remediation": "Add descriptive text between <a>...</a> or use aria-label/title if it's an icon link.",
                "wcag_reference": "2.4.4",
                "impact": "Screen reader or keyboard-only users cannot determine the purpose of the link.",
                "page_url": page_url,
                "element_info": get_element_info(link, html_lines=lines)
            })
            continue

        if lower_text in AMBIGUOUS_LINK_TEXT:
            raw_incidences.append({
                "title": "Ambiguous or generic link text",
                "type": "Link Purpose",
                "severity": "Medium",
                "expected_result": "Links must describe their purpose in context.",
                "actual_result": f"The link text is too generic: \"{link_text}\"",
                "remediation": (
                    "Use specific text, e.g. 'Download the annual report' instead of 'click here'. "
                    "Or ensure the link is accompanied by contextual text on the same line/paragraph."
                ),
                "wcag_reference": "2.4.4",
                "impact": (
                    "Users who browse links out of context (e.g., with a screen reader) "
                    "cannot discern the purpose of the link."
                ),
                "page_url": page_url,
                "element_info": get_element_info(link, html_lines=lines)
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
            "Failed checkpoint": "2.4.4",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
