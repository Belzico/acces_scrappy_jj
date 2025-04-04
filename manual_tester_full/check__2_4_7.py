from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_html_lines(html_content):
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    return "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))

def get_element_info(element, html_lines=None):
    tag = element.name
    text = element.get_text(strip=True)[:50]
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    snippet = ""
    if line_number != "N/A" and html_lines:
        try:
            snippet = get_line_snippet(html_lines, int(line_number))
        except Exception:
            snippet = str(element)[:300]

    return {
        "tag": tag,
        "text": text,
        "line_number": line_number,
        "evidence": snippet
    }

def format_incidence(old):
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {old.get('element_info', {}).get('tag')}\n"
            "3. Press TAB repeatedly and verify the visible focus indicator appears correctly."
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("expected_result"),
        "Actual Result": old.get("actual_result"),
        "Suggested resolution(s)": old.get("remediation"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact"),
        "Evidence [SS or Video]": old.get("element_info", {}).get("evidence", "N/A")
    }

def check_focus_visible(html_content, page_url, html_lines):
    soup = BeautifulSoup(html_content, "html.parser")
    focusable_elements = soup.find_all(["a", "button", "input", "select", "textarea", "iframe", "div", "span"])
    raw_incidences = []

    for element in focusable_elements:
        info = get_element_info(element, html_lines)
        styles = element.get("style", "").lower()

        if "outline:none" in styles or "outline: 0" in styles or "border: none" in styles:
            raw_incidences.append({
                "title": "Element without visible focus indicator",
                "type": "Focus Visibility",
                "severity": "High",
                "expected_result": "The element should display a visible focus indicator when selected.",
                "actual_result": f"The element hides focus using styles: {styles}",
                "remediation": "Ensure focus is visible by adding `:focus` or `:focus-visible` in CSS.",
                "wcag_reference": "2.4.7",
                "impact": "Keyboard users cannot see which element is focused.",
                "page_url": page_url,
                "element_info": info
            })

        if element.name in ["div", "span"] and ("onclick" in element.attrs or "role" in element.attrs):
            if "tabindex" not in element.attrs:
                raw_incidences.append({
                    "title": "Interactive element without tabindex",
                    "type": "Focus Visibility",
                    "severity": "Medium",
                    "expected_result": "Interactive elements must be keyboard-focusable via `tabindex='0'`.",
                    "actual_result": f"The <{element.name}> element is interactive but lacks `tabindex`.",
                    "remediation": "Add `tabindex='0'` so it can receive keyboard focus.",
                    "wcag_reference": "2.4.7",
                    "impact": "Keyboard users cannot access this element.",
                    "page_url": page_url,
                    "element_info": info
                })

        if element.attrs.get("tabindex") == "-1":
            raw_incidences.append({
                "title": "Element with tabindex='-1'",
                "type": "Focus Visibility",
                "severity": "Medium",
                "expected_result": "The element should be reachable via keyboard unless explicitly excluded.",
                "actual_result": "The element is removed from keyboard navigation via `tabindex='-1'`.",
                "remediation": "Avoid using `tabindex='-1'` unless an accessible alternative is provided.",
                "wcag_reference": "2.4.7",
                "impact": "The element will not be accessible via keyboard.",
                "page_url": page_url,
                "element_info": info
            })

        if "display:none" in styles or "visibility:hidden" in styles:
            raw_incidences.append({
                "title": "Element hidden when receiving focus",
                "type": "Focus Visibility",
                "severity": "High",
                "expected_result": "Elements should remain visible when focused.",
                "actual_result": f"The element is hidden via CSS: {styles}",
                "remediation": "Ensure the element remains visible when it receives focus.",
                "wcag_reference": "2.4.7",
                "impact": "Users may lose navigation context.",
                "page_url": page_url,
                "element_info": info
            })

    return raw_incidences

def run_all___2_4_7(html_content, page_url, excel="issue_report.xlsx"):
    html_lines = get_html_lines(html_content)
    raw = check_focus_visible(html_content, page_url, html_lines)
    formatted = [format_incidence(i) for i in raw]

    if not formatted:
        formatted.append({
            "Title": "Justificación de los CPs asignados que no generen issues",
            "Steps": "N/A",
            "Bug Type": "N/A",
            "Priority": "N/A",
            "Expected Result": "N/A",
            "Actual Result": "N/A",
            "Suggested resolution(s)": "N/A",
            "Failed checkpoint": "2.4.7",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
