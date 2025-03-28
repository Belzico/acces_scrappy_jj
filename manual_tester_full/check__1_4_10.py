from bs4 import BeautifulSoup
import re
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
            f"3. Review its styles affecting width and reflow at 320px."
        ),
        "Bug Type": issue.get("type"),
        "Priority": issue.get("severity"),
        "Expected Result": issue.get("expected_result", "N/A"),
        "Actual Result": issue.get("actual_result", "N/A"),
        "Suggested resolution(s)": issue.get("remediation"),
        "Failed checkpoint": issue.get("wcag_reference"),
        "User Impact": issue.get("impact", "N/A"),
        "Evidence [SS or Video]": issue.get("element_info", {}).get("evidence", "N/A")
    }


def run_all___1_4_10(html_content, page_url, excel="issue_report.xlsx"):
    """
    Valida WCAG 1.4.10 (Reflow) para detectar:
    - Estilos de ancho fijo que impiden el reflow.
    - Desplazamiento horizontal forzado.
    - Estilos embebidos con `width: Xpx` sin `max-width`.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 1️⃣ Elementos con `style="width: XXXpx"` sin `max-width`
    for tag in soup.find_all(style=True):
        style = tag["style"].lower()
        if re.search(r"width\s*:\s*\d+px", style) and "max-width" not in style:
            raw_incidences.append({
                "title": "Fixed width element detected (inline styles)",
                "type": "Zoom",
                "severity": "High",
                "expected_result": "Content should adapt to a 320px viewport without requiring horizontal scroll.",
                "actual_result": "Element has fixed width (e.g., `width: 600px`) and lacks `max-width`.",
                "remediation": "Use `max-width: 100%`, `flexbox`, or `grid` instead of fixed widths.",
                "wcag_reference": "1.4.10",
                "impact": "Users will need to scroll horizontally to read content.",
                "page_url": page_url,
                "element_info": get_element_info(tag)
            })

    # 2️⃣ Estilos embebidos en <style> con `width: XXXpx` sin `max-width`
    for style_tag in soup.find_all("style"):
        css_text = style_tag.get_text()
        lines = css_text.split(";")

        for rule in lines:
            if re.search(r"width\s*:\s*\d+px", rule) and "max-width" not in rule:
                raw_incidences.append({
                    "title": "Fixed width detected in embedded CSS",
                    "type": "Zoom",
                    "severity": "High",
                    "expected_result": "CSS rules should use responsive width declarations.",
                    "actual_result": "Rule contains `width: XXXpx` without `max-width`.",
                    "remediation": "Use `max-width: 100%` or relative units like %, em, rem.",
                    "wcag_reference": "1.4.10",
                    "impact": "Content may overflow on small viewports like 320px.",
                    "page_url": page_url,
                    "element_info": get_element_info(style_tag)
                })

    # 3️⃣ Estilos con `overflow-x: auto` o `scroll`
    for tag in soup.find_all(style=True):
        style = tag["style"].lower()
        if "overflow-x: auto" in style or "overflow-x: scroll" in style:
            raw_incidences.append({
                "title": "Horizontal scrolling detected",
                "type": "Zoom",
                "severity": "High",
                "expected_result": "Content should reflow and eliminate horizontal scroll at 320px width.",
                "actual_result": "Element enables `overflow-x: auto` or `scroll`, forcing horizontal scroll.",
                "remediation": "Remove horizontal scroll and use fluid layout with `max-width: 100%`.",
                "wcag_reference": "1.4.10",
                "impact": "Navigation becomes difficult on small screens.",
                "page_url": page_url,
                "element_info": get_element_info(tag)
            })

    formatted = [format_incidence(inc) for inc in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)

    return formatted
