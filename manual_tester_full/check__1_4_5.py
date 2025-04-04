from bs4 import BeautifulSoup, NavigableString
import os
import pytesseract
from PIL import Image
from transform_json_to_excel import transform_json_to_excel

def get_html_lines(html_content):
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(
        f"{i+1}: {snippet[i - start]}"
        for i in range(start, end)
    )
    return snippet_str

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

    evidence_str = ", ".join(evidence_parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_str else f"{tag}[src]"

    snippet_str = ""
    if line_number != "N/A" and html_lines:
        try:
            line_int = int(line_number)
            snippet_str = get_line_snippet(html_lines, line_int, context=2)
        except ValueError:
            pass

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence,
        "fragment_html": snippet_str
    }

def format_incidence(raw_inc):
    element_info = raw_inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")

    return {
        "Title": raw_inc.get("title"),
        "Steps": (
            f"1. Open the page: {raw_inc.get('page_url')}\n"
            f"2. Inspect the element: {element_info.get('tag', 'N/A')}\n"
            f"3. Compare the OCR text with the <img>'s alt or nearby text.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n"
            f"{snippet}"
        ),
        "Bug Type": raw_inc.get("type"),
        "Priority": raw_inc.get("severity"),
        "Expected Result": raw_inc.get("expected_result", "N/A"),
        "Actual Result": raw_inc.get("actual_result", "N/A"),
        "Suggested resolution(s)": raw_inc.get("remediation"),
        "Failed checkpoint": raw_inc.get("wcag_reference"),
        "User Impact": raw_inc.get("impact", "N/A"),
        "Evidence [SS or Video]": element_info.get("evidence", "N/A")
    }

def run_all___1_4_5(html_content, page_url, images_folder="downloaded_images", excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue

        filename = os.path.basename(src)
        local_path = os.path.join(images_folder, filename)

        if not os.path.isfile(local_path):
            continue

        try:
            text_extracted = pytesseract.image_to_string(Image.open(local_path)).strip()
        except Exception:
            continue  # Si OCR falla, omitimos la imagen

        if text_extracted:
            alt_value = img.get("alt", "")
            sibling_text_nodes = []
            for sibling in img.next_siblings:
                if isinstance(sibling, NavigableString):
                    sibling_text_nodes.append(str(sibling))
            sibling_text = "".join(sibling_text_nodes).lower()
            combined_text = (alt_value + sibling_text).lower()

            if text_extracted.lower() not in combined_text:
                info = get_element_info(img, html_lines=lines)
                raw_incidences.append({
                    "title": "Image of Text Possibly Used",
                    "type": "Screen Reader",
                    "severity": "High",
                    "expected_result": (
                        "All textual content in images should be available as real HTML text, "
                        "or at least replicated in the alt attribute or nearby content."
                    ),
                    "actual_result": (
                        f"OCR detected text: '{text_extracted[:60]}...', but no equivalent text was found nearby."
                    ),
                    "remediation": (
                        "Use HTML text instead of an image when possible. If unavoidable, "
                        "ensure the alt attribute or nearby text includes the same content."
                    ),
                    "wcag_reference": "1.4.5",
                    "impact": "Screen reader or zoom users may miss important visual text.",
                    "page_url": page_url,
                    "element_info": info
                })

    formatted_incidences = [format_incidence(inc) for inc in raw_incidences]
    if formatted_incidences:
        transform_json_to_excel(formatted_incidences, excel)

    return formatted_incidences
