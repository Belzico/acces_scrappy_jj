from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel


def get_element_info(element):
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    evidence_parts = []
    if classes:
        evidence_parts.append(f"class={classes}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")

    evidence = f"{tag}[{', '.join(evidence_parts)}]" if evidence_parts else tag

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }


def format_incidence(issue):
    return {
        "Title": issue.get("title"),
        "Steps": (
            f"1. Open the page: {issue.get('page_url')}\n"
            f"2. Inspect the element: {issue.get('element_info', {}).get('tag', 'N/A')}\n"
            f"3. Zoom the page to 200% and verify if text remains visible."
        ),
        "Bug Type": issue.get("type"),
        "Priority": issue.get("severity"),
        "Expected Result": issue.get("expected_result", "Text should remain fully visible when zoomed to 200%."),
        "Actual Result": issue.get("actual_result", "Text may be cropped, hidden, or truncated."),
        "Suggested resolution(s)": issue.get("remediation"),
        "Failed checkpoint": issue.get("wcag_reference"),
        "User Impact": issue.get("impact"),
        "Evidence [SS or Video]": issue.get("element_info", {}).get("evidence", "N/A")
    }


def run_all___1_4_4(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 1️⃣ Inline styles: overflow/height issues
    for tag in soup.find_all(style=True):
        style = tag["style"].lower()
        if "overflow: hidden" in style or "height:" in style or "max-height:" in style:
            raw_incidences.append({
                "title": "Text may be cut off at 200% zoom",
                "type": "Zoom",
                "severity": "High",
                "expected_result": "Text should remain fully visible when zoomed to 200%.",
                "actual_result": "Element uses `overflow: hidden`, `height`, or `max-height` which may cause clipping.",
                "remediation": "Avoid fixed height/overflow on text containers. Use flexible layouts.",
                "wcag_reference": "1.4.4",
                "impact": "Important information may be lost during zoom.",
                "page_url": page_url,
                "element_info": get_element_info(tag)
            })

    # 2️⃣ CSS classes: text truncation
    problematic_classes = {"hidden", "truncate", "text-cutoff", "text-hidden"}
    for tag in soup.find_all(class_=True):
        tag_classes = set(tag.get("class", []))
        matched = tag_classes & problematic_classes

        if matched:
            raw_incidences.append({
                "title": "Text truncation detected via CSS classes",
                "type": "Zoom",
                "severity": "High",
                "expected_result": "All text should remain fully readable when zoomed.",
                "actual_result": f"Element uses class(es) {matched}, which may truncate or hide text.",
                "remediation": "Remove or override truncation classes to allow text expansion.",
                "wcag_reference": "1.4.4",
                "impact": "Text may not be visible when enlarged.",
                "page_url": page_url,
                "element_info": get_element_info(tag)
            })

    formatted = [format_incidence(inc) for inc in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)

    return formatted
