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
    tag = element.name
    attrs = dict(element.attrs)
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    snippet_str = ""
    if line_number != "N/A" and html_lines:
        try:
            snippet_str = get_line_snippet(html_lines, int(line_number))
        except ValueError:
            pass

    return {
        "tag": tag,
        "attrs": attrs,
        "snippet": str(element)[:300],
        "line_number": line_number,
        "fragment_html": snippet_str
    }

def format_incidence(inc):
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Check if moving, blinking, scrolling or auto-updating content "
            "has controls to pause, stop or hide it.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n"
            f"{snippet}"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": element_info.get("snippet", "")
    }

def run_all___2_2_2(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    target_elements = soup.find_all(
        lambda tag: (
            tag.name in ["marquee", "blink"] or
            "scroll" in tag.get("class", []) or
            tag.has_attr("scrollamount") or
            tag.has_attr("behavior") or
            "animation" in str(tag.get("style", "")).lower()
        )
    )

    for elem in target_elements:
        has_control = soup.find(
            lambda t: t.name in ["button", "a"] and
            any(k in t.get_text(strip=True).lower() for k in ["pause", "stop", "hide"])
        )

        if not has_control:
            raw_incidences.append({
                "title": "No controls found to pause/stop/hide animated or auto-updated content",
                "type": "Moving/Blinking/Auto-updating Content",
                "severity": "High",
                "expected_result": (
                    "Any moving, blinking, scrolling or auto-updating content "
                    "should have a visible control to pause, stop, or hide it."
                ),
                "actual_result": (
                    f"Found animated or scrolling element ({elem.name}) without a clear mechanism to pause, stop or hide."
                ),
                "remediation": (
                    "Add a control (button, link, etc.) near the moving content "
                    "to allow users to pause, stop, or hide it."
                ),
                "wcag_reference": "2.2.2",
                "impact": (
                    "Content in motion can be distracting and prevent users, especially "
                    "those with cognitive disabilities, from reading or interacting with the page."
                ),
                "page_url": page_url,
                "element_info": get_element_info(elem, html_lines=lines)
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
            "Failed checkpoint": "2.2.2",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
