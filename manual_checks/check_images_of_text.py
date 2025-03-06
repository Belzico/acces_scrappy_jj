from bs4 import BeautifulSoup, NavigableString
import os
import pytesseract
from PIL import Image
from transform_json_to_excel import transform_json_to_excel  

def check_images_of_text(html_content, page_url, images_folder="downloaded_images", excel="issue_report.xlsx"):
    """
    Checks if images contain text (OCR) and verifies if there is nearby 
    real text that matches it.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue

        filename = os.path.basename(src)
        local_path = os.path.join(images_folder, filename)

        if not os.path.isfile(local_path):
            # Skip OCR if the image file does not exist locally
            continue
        
        # OCR Processing
        try:
            text_extracted = pytesseract.image_to_string(Image.open(local_path)).strip()
        except Exception as e:
            incidences.append({
                "title": "OCR processing error",
                "type": "Test Execution",
                "severity": "Medium",
                "description": f"OCR processing failed for '{src}': {e}",
                "remediation": "Check Tesseract installation or improve image readability.",
                "wcag_reference": None,
                "impact": "No textual comparison was possible for that image.",
                "page_url": page_url,
                "resolution": "check_images_of_text.md"
            })
            continue
        
        # If text is found in the image
        if text_extracted:
            # Check the alt attribute
            alt_value = img.get("alt", "")

            # Extract only text nodes (NavigableString) from sibling elements
            sibling_text_nodes = []
            for sibling in img.next_siblings:
                if isinstance(sibling, NavigableString):
                    sibling_text_nodes.append(str(sibling))

            sibling_text = "".join(sibling_text_nodes)

            # Check if the extracted text is missing from alt + nearby text
            combined_text = (alt_value + sibling_text).lower()
            if text_extracted.lower() not in combined_text:
                incidences.append({
                    "title": "Image of Text Possibly Used",
                    "type": "Screen Reader",
                    "severity": "High",
                    "description": (
                        f"The image '{src}' contains text (OCR detected): '{text_extracted[:60]}...' "
                        "but there is no equivalent textual content in the HTML. This suggests an image of text "
                        "without a real text alternative.\n"
                        "Reference: WCAG 1.4.5: Images of Text."
                    ),
                    "remediation": (
                        "Use real HTML text instead of an image when possible. If an image is necessary, "
                        "provide an alternative text version (Technique C30)."
                    ),
                    "wcag_reference": "1.4.5",
                    "impact": "Users who rely on screen readers or zoom may struggle to access the text.",
                    "page_url": page_url,
                    "resolution": "check_images_of_text.md"
                })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
