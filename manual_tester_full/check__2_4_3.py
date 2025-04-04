from bs4 import BeautifulSoup
import re
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
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    evidence_parts = []
    if classes:
        evidence_parts.append(f"class={classes}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")
    evidence = f"{tag}[{', '.join(evidence_parts)}]" if evidence_parts else tag

    snippet = ""
    if line_number != "N/A" and html_lines:
        try:
            snippet = get_line_snippet(html_lines, int(line_number))
        except Exception:
            pass

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence,
        "fragment_html": snippet
    }

def format_incidence(old):
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {old.get('element_info', {}).get('tag', 'N/A')}\n"
            f"3. Check the focus behavior and tab order.\n\n"
            f"HTML snippet (around line {old.get('element_info', {}).get('line_number', 'N/A')}):\n"
            f"{old.get('element_info', {}).get('fragment_html', '')}"
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("expected_result", "N/A"),
        "Actual Result": old.get("actual_result", "N/A"),
        "Suggested resolution(s)": old.get("remediation"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact", "N/A"),
        "Evidence [SS or Video]": old.get("element_info", {}).get("evidence", "N/A")
    }

def run_all___2_4_3(html_content, page_url, excel="issue_report.xlsx"):
    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)

    # 1️⃣ tabindex > 0
    elements_with_tabindex = soup.find_all(lambda tag: tag.has_attr("tabindex"))
    for element in elements_with_tabindex:
        tabindex_value = element.get("tabindex")
        if tabindex_value and tabindex_value.isdigit():
            tabindex_value = int(tabindex_value)
            if tabindex_value > 0:
                incidences.append({
                    "title": "Use of tabindex greater than 0",
                    "type": "Focus Order",
                    "severity": "High",
                    "expected_result": "Elements should follow natural DOM focus order or use tabindex=0 when needed.",
                    "actual_result": f"The element has tabindex={tabindex_value}, disrupting the natural focus flow.",
                    "remediation": "Avoid using tabindex greater than 0. Use the natural DOM order.",
                    "wcag_reference": "2.4.3",
                    "impact": "The focus order may become unpredictable.",
                    "page_url": page_url,
                    "resolution": "check_focus_order.md",
                    "element_info": get_element_info(element, html_lines=lines)
                })

        if str(tabindex_value) == "-1" and element.name in ["a", "button", "input", "textarea", "select"]:
            incidences.append({
                "title": "Interactive element with tabindex=-1",
                "type": "Focus Order",
                "severity": "Medium",
                "expected_result": "Interactive elements should be reachable via Tab unless managed by JS.",
                "actual_result": "The element has tabindex=-1, making it unreachable via keyboard.",
                "remediation": "Avoid using tabindex=-1 on interactive elements unless managed with JavaScript.",
                "wcag_reference": "2.4.3",
                "impact": "Users cannot access this element using the keyboard.",
                "page_url": page_url,
                "resolution": "check_focus_order.md",
                "element_info": get_element_info(element, html_lines=lines)
            })

    # 2️⃣ <a> sin href y sin tabindex
    interactive_elements = soup.find_all(["a", "button", "input", "textarea", "select"])
    for element in interactive_elements:
        if not element.has_attr("tabindex") and element.name == "a" and not element.has_attr("href"):
            incidences.append({
                "title": "Link without href and without tabindex",
                "type": "Focus Order",
                "severity": "Medium",
                "expected_result": "<a> elements should have href or tabindex to be focusable.",
                "actual_result": "The <a> element has no href or tabindex, making it non-focusable.",
                "remediation": "Add an href or a tabindex=0 if it needs to be focusable.",
                "wcag_reference": "2.4.3",
                "impact": "Keyboard users will not be able to access the link.",
                "page_url": page_url,
                "resolution": "check_focus_order.md",
                "element_info": get_element_info(element, html_lines=lines)
            })

    # 3️⃣ <dialog> sin atributo open
    dialogs = soup.find_all("dialog")
    for dialog in dialogs:
        if not dialog.has_attr("open"):
            incidences.append({
                "title": "Modal (dialog) without 'open' attribute",
                "type": "Focus Order",
                "severity": "Low",
                "expected_result": "Visible modals should include the 'open' attribute to manage focus properly.",
                "actual_result": "The <dialog> is missing the 'open' attribute, which may affect accessibility.",
                "remediation": "Ensure the dialog has the 'open' attribute when visible and correctly manages focus.",
                "wcag_reference": "2.4.3",
                "impact": "Users may not realize that the modal is active.",
                "page_url": page_url,
                "resolution": "check_focus_order.md",
                "element_info": get_element_info(dialog, html_lines=lines)
            })

    formatted = [format_incidence(inc) for inc in incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)
    return formatted
