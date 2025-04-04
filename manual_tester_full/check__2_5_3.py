import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_html_lines(html_content):
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))
    return snippet_str

def get_element_info(element, html_lines=None):
    tag = element.name
    text = element.get_text(strip=True)[:80]
    evidence = str(element)[:300]
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"
    fragment_html = ""

    if line_number != "N/A" and html_lines:
        try:
            fragment_html = get_line_snippet(html_lines, int(line_number), context=2)
        except Exception:
            fragment_html = ""

    return {
        "tag": tag,
        "text": text,
        "evidence": evidence,
        "line_number": line_number,
        "fragment_html": fragment_html
    }

def format_incidence(inc):
    element_info = inc.get("element_info", {})
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the element \"{element_info.get('tag')}\".\n"
            f"3. HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n"
            f"{element_info.get('fragment_html', '')}"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": element_info.get("evidence", "")
    }

def run_all___2_5_3(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    html_lines = get_html_lines(html_content)
    raw_incidences = []

    buttons = soup.find_all("button")
    for btn in buttons:
        visible_text = btn.get_text(strip=True)
        aria_label = btn.get("aria-label", "")
        if aria_label:
            if visible_text and visible_text.lower() not in aria_label.lower():
                raw_incidences.append({
                    "title": "Button label mismatch",
                    "type": "Label in Name",
                    "severity": "Medium",
                    "expected_result": "The visible text of the button should be included in the aria-label.",
                    "actual_result": f"Visible: '{visible_text}', aria-label: '{aria_label}'",
                    "remediation": "Ensure aria-label includes the visible text or remove aria-label if unneeded.",
                    "wcag_reference": "2.5.3",
                    "impact": "Voice users may say the visible text and fail to activate the button.",
                    "page_url": page_url,
                    "element_info": get_element_info(btn, html_lines)
                })
        else:
            if not visible_text:
                raw_incidences.append({
                    "title": "Button has no visible label nor aria-label",
                    "type": "Label in Name",
                    "severity": "High",
                    "expected_result": "Buttons must have a visible text or an aria-label that matches it.",
                    "actual_result": "No text and no aria-label found.",
                    "remediation": "Add text inside the button or set an aria-label attribute.",
                    "wcag_reference": "2.5.3",
                    "impact": "Users cannot identify or activate the button by name.",
                    "page_url": page_url,
                    "element_info": get_element_info(btn, html_lines)
                })

    inputs = soup.find_all("input", {"type": ["button", "submit", "reset", "image"]})
    for inp in inputs:
        value_text = inp.get("value", "")
        aria_label = inp.get("aria-label", "")
        alt_text = inp.get("alt", "")
        visible_text = alt_text if inp.get("type") == "image" else value_text
        if aria_label:
            if visible_text and visible_text.lower() not in aria_label.lower():
                raw_incidences.append({
                    "title": "Input button label mismatch",
                    "type": "Label in Name",
                    "severity": "Medium",
                    "expected_result": "The visible text of the input should be included in the aria-label.",
                    "actual_result": f"Visible: '{visible_text}', aria-label: '{aria_label}'",
                    "remediation": "Ensure aria-label includes the visible text or remove aria-label if unneeded.",
                    "wcag_reference": "2.5.3",
                    "impact": "Voice input users may fail to activate the control.",
                    "page_url": page_url,
                    "element_info": get_element_info(inp, html_lines)
                })
        else:
            if not visible_text:
                raw_incidences.append({
                    "title": "Input button has no visible text nor aria-label",
                    "type": "Label in Name",
                    "severity": "High",
                    "expected_result": "A button or image input must have a label for users.",
                    "actual_result": "No 'value', no 'alt', and no 'aria-label'.",
                    "remediation": "Add a 'value', alt text, or aria-label.",
                    "wcag_reference": "2.5.3",
                    "impact": "Users cannot invoke the control by voice command using the visible label.",
                    "page_url": page_url,
                    "element_info": get_element_info(inp, html_lines)
                })

    labels = soup.find_all("label")
    for lbl in labels:
        label_text = lbl.get_text(strip=True)
        if not label_text:
            continue
        for_id = lbl.get("for")
        if for_id:
            input_el = soup.find(id=for_id)
            if input_el:
                aria_label = input_el.get("aria-label", "")
                if aria_label and label_text.lower() not in aria_label.lower():
                    raw_incidences.append({
                        "title": "Form label mismatch",
                        "type": "Label in Name",
                        "severity": "Medium",
                        "expected_result": "The visible label text should be included in the aria-label.",
                        "actual_result": f"Label text: '{label_text}', aria-label: '{aria_label}'",
                        "remediation": "Match them or remove aria-label if label element is correctly associated.",
                        "wcag_reference": "2.5.3",
                        "impact": "Voice users might not be recognized when referring to the input.",
                        "page_url": page_url,
                        "element_info": get_element_info(input_el, html_lines)
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
            "Failed checkpoint": "2.5.3",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
