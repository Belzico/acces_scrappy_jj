from bs4 import BeautifulSoup, NavigableString
import os
import pytesseract
from PIL import Image
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
    evidence = f"{tag}[{evidence_parts and evidence_str or 'src'}]"

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }

def format_incidence(raw_inc):
    return {
        "Title": raw_inc.get("title"),
        "Steps": (
            f"1. Open the page: {raw_inc.get('page_url')}\n"
            f"2. Inspect the element: {raw_inc.get('element_info', {}).get('tag', 'N/A')}\n"
            f"3. Compare the OCR text with the <img>'s alt or nearby text."
        ),
        "Bug Type": raw_inc.get("type"),
        "Priority": raw_inc.get("severity"),
        "Expected Result": raw_inc.get("expected_result", "N/A"),
        "Actual Result": raw_inc.get("actual_result", "N/A"),
        "Suggested resolution(s)": raw_inc.get("remediation"),
        "Failed checkpoint": raw_inc.get("wcag_reference"),
        "User Impact": raw_inc.get("impact", "N/A"),
        "Evidence [SS or Video]": raw_inc.get("element_info", {}).get("evidence", "N/A")
    }

def run_all___1_4_5(html_content, page_url, images_folder="downloaded_images", excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
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
            # Si OCR falla, simplemente omitir la imagen
            continue

        if text_extracted:
            alt_value = img.get("alt", "")
            sibling_text_nodes = []
            for sibling in img.next_siblings:
                if isinstance(sibling, NavigableString):
                    sibling_text_nodes.append(str(sibling))
            sibling_text = "".join(sibling_text_nodes).lower()
            combined_text = (alt_value + sibling_text).lower()

            if text_extracted.lower() not in combined_text:
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
                    "element_info": get_element_info(img)
                })

    formatted_incidences = [format_incidence(inc) for inc in raw_incidences]
    if formatted_incidences:
        transform_json_to_excel(formatted_incidences, excel)

    return formatted_incidences
