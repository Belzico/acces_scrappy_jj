# manual_checks/check_informative_images.py

import os
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
from transform_json_to_excel import transform_json_to_excel  

def check_informative_images(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if informative images have appropriate alt text and, optionally,
    compares actual text (via OCR) with the alt text.
    
    - Searches for images in the 'downloaded_images' folder.
    - If the alt attribute is missing or empty -> Error.
    - If the alt is generic (e.g., "image") -> Warning.
    - Applies OCR if the image exists in 'downloaded_images' and compares it with the alt text.

    Based on W3C official documentation for “Informative Images”:
    https://www.w3.org/WAI/tutorials/images/informative/

    Requirements:
      - Tesseract installed, 'pytesseract' and 'Pillow' in your environment.
      - Ensure images are downloaded to:
        'downloaded_images/<filename>'

    Returns a list of detected issues.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # Generic alt text words that do not provide meaningful information
    GENERIC_WORDS = {"image", "photo", "picture", "graphic", "icon", "logo"}

    for img in soup.find_all("img"):
        src_attr = img.get("src") or ""
        alt_value = img.get("alt")

        # 🚨 1) Missing or empty alt attribute
        if alt_value is None or alt_value.strip() == "":
            incidences.append({
                "title": "Informative image with missing or empty alt",
                "type": "Screen Reader",
                "severity": "High",
                "description": (
                    f"The image '{src_attr}' (informative) has no or empty alt attribute. "
                    "Screen reader users won't perceive the information.\n"
                    "Reference: https://www.w3.org/WAI/tutorials/images/informative/"
                ),
                "remediation": (
                    "Add a short, meaningful alt text that conveys the message.\n"
                    "Example: `<img src='cap.png' alt='Push the cap down and turn it counter-clockwise...'>`"
                ),
                "wcag_reference": "1.1.1",
                "impact": "Essential information is lost for screen reader users.",
                "page_url": page_url,
                "resolution": "check_informative_images.md"
            })
            continue

        alt_stripped = alt_value.strip()
        alt_lower = alt_stripped.lower()

        # 🚨 2) Generic alt text (e.g., “image”, “photo”, “icon”)
        if alt_lower in GENERIC_WORDS or alt_lower in {f"an {w}" for w in GENERIC_WORDS}:
            incidences.append({
                "title": "Informative image has a generic alt text",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    f"The image '{src_attr}' uses a generic alt '{alt_stripped}', "
                    "which doesn't convey the actual meaning.\n"
                    "Reference: https://www.w3.org/WAI/tutorials/images/informative/"
                ),
                "remediation": (
                    "Use a short phrase describing the content.\n"
                    "Example: `<img src='dog.jpg' alt='Dog with a bell attached to its collar.'>`"
                ),
                "wcag_reference": "1.1.1",
                "impact": "Screen reader users receive a non-informative label instead of actual content.",
                "page_url": page_url,
                "resolution": "check_informative_images.md"
            })
            # Continue processing to check OCR comparison.

        # 🚨 3) Locate the image in the 'downloaded_images' folder
        image_filename = os.path.basename(src_attr)  
        local_path = os.path.join("downloaded_images", image_filename)

        if not os.path.isfile(local_path):
            # If the image is not available locally, skip OCR
            continue

        # 🚨 4) Perform OCR text extraction
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

        try:
            text_extracted = pytesseract.image_to_string(Image.open(local_path)).strip()
        except Exception as e:
            incidences.append({
                "title": "OCR processing error",
                "type": "Test Execution",
                "severity": "Medium",
                "description": f"OCR processing failed for '{local_path}'. Error: {e}",
                "remediation": "Check Tesseract installation or improve image readability.",
                "wcag_reference": None,
                "impact": "No textual comparison was possible for that image.",
                "page_url": page_url,
                "resolution": "check_informative_images.md"
            })
            continue

        # 🚨 5) Compare extracted text with alt text
        if text_extracted:
            ocr_lower = text_extracted.lower()
            set_ocr = set(ocr_lower.split())
            set_alt = set(alt_lower.split())

            similarity = len(set_ocr & set_alt) / len(set_ocr) if set_ocr else 0.0

            if similarity < 0.3:
                incidences.append({
                    "title": "Alt text may be inaccurate compared to image text",
                    "type": "Screen Reader",
                    "severity": "Medium",
                    "description": (
                        f"Image: '{local_path}'\n"
                        f"OCR text: '{text_extracted[:80]}...'\n"  
                        f"Alt: '{alt_stripped}'\n"
                        f"Text match: {similarity*100:.1f}%\n\n"
                        "This suggests that the alt text does not properly match the essential text in the image.\n"
                        "Reference: https://www.w3.org/WAI/tutorials/images/informative/"
                    ),
                    "remediation": (
                        "Update the alt text to properly reflect the text in the image (if that text is relevant)."
                    ),
                    "wcag_reference": "1.1.1",
                    "impact": "Screen reader users receive an alt text that does not match the real text in the image.",
                    "page_url": page_url,
                    "resolution": "check_informative_images.md"
                })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
