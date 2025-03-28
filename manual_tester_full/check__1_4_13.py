from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel


def get_element_info(element):
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

    evidence_str = ", ".join(evidence_parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_str else tag

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }


def format_incidence(old):
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {old.get('element_info', {}).get('tag', 'N/A')}\n"
            "3. Check if the additional content meets dismissible, hoverable, and persistent requirements."
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("expected_result", "N/A"),
        "Actual Result": old.get("actual_result", "N/A"),
        "Suggested resolution(s)": old.get("Suggested resolution(s)"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact", "N/A"),
        "Evidence [SS or Video]": old.get("element_info", {}).get("evidence", "N/A")
    }


def run_all___1_4_13(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []
    checked_elements = set()

    def is_candidate(el):
        class_check = any(cls in ["tooltip", "popover", "popup", "hint", "hover"]
                          for cls in el.get("class", [])) if el.has_attr("class") else False
        return (
            el.get("role") == "tooltip" or
            el.has_attr("data-tooltip") or
            el.has_attr("aria-hidden") or
            el.has_attr("data-popup") or
            el.has_attr("data-hover") or
            el.has_attr("aria-describedby") or
            class_check
        )

    # Recolectar elementos directamente candidatos
    tooltip_candidates = [el for el in soup.find_all() if is_candidate(el)]

    # Incluir elementos referenciados por aria-describedby
    for el in soup.find_all(attrs={"aria-describedby": True}):
        ref_id = el.get("aria-describedby")
        referenced = soup.find(id=ref_id)
        if referenced and referenced not in tooltip_candidates:
            tooltip_candidates.append(referenced)

    # Procesar los candidatos
    for element in tooltip_candidates:
        if str(element) in checked_elements:
            continue
        checked_elements.add(str(element))

        style = element.get("style", "").lower()
        info = get_element_info(element)

        dismissible = "escape" in style or "dismiss" in style
        hoverable = "pointer-events" in style or "hover" in style
        persistent = not any(term in style for term in ["timeout", "fadeout", "display:none"])

        fails = []
        if not dismissible:
            fails.append("Content does not provide a clear method for dismissal (e.g., Escape key or close button).")
        if not hoverable:
            fails.append("Content may disappear when the pointer moves off the trigger (not hoverable).")
        if not persistent:
            fails.append("Content appears to auto-hide or lacks persistence after appearing.")

        if fails:
            raw_incidences.append({
                "title": "Hover/Focus-triggered content may violate WCAG 1.4.13",
                "type": "Focus & Hover Interaction",
                "severity": "Medium",
                "expected_result": (
                    "Additional content triggered by hover or focus must be:\n"
                    "- Dismissible (can be closed without moving focus/mouse),\n"
                    "- Hoverable (does not disappear when hovered), and\n"
                    "- Persistent (remains visible until dismissed or unfocused)."
                ),
                "actual_result": " | ".join(fails),
                "Suggested resolution(s)": (
                    "Ensure the content can be dismissed using Escape or a button, remains visible "
                    "while hovered, and does not automatically disappear unless invalidated."
                ),
                "wcag_reference": "1.4.13",
                "impact": (
                    "Users with low vision or motor disabilities may not be able to read, interact with, "
                    "or dismiss the content appropriately, causing confusion or interruption."
                ),
                "page_url": page_url,
                "element_info": info
            })

    formatted = [format_incidence(inc) for inc in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)
    return formatted
