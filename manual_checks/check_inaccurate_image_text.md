# 🏷️ Check for Informative Images Accessibility  

## 📌 Overview  
This script detects accessibility issues with informative images in an HTML document. It ensures that images conveying information have appropriate `alt` attributes and, optionally, compares the image text (via OCR) with the `alt` text to detect discrepancies.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Informative images (`<img>`)** missing an `alt` attribute.  
- **Images with generic `alt` text** (e.g., "image", "photo", "icon") that do not provide meaningful descriptions.  
- **Images with mismatched `alt` text and actual image text** using Optical Character Recognition (OCR).  
- **Exports the findings to Excel (`issue_report.xlsx`).**  

## 🚀 Installation  
Make sure you have the required dependencies installed:  

```sh
pip install beautifulsoup4 pytesseract pillow openpyxl
🔧 Additional Setup
You need to install Tesseract OCR to enable text extraction from images:

Windows: Download and install from Tesseract OCR.
Linux/macOS: Install via package manager (sudo apt install tesseract-ocr or brew install tesseract).
After installation, update the script's pytesseract.pytesseract.tesseract_cmd path if necessary.

🖥️ Usage
To run the script, provide an HTML string and a page URL:

python
Copy
Edit
from check_informative_images import check_informative_images

html_content = """
<html>
    <body>
        <img src="informative.png" alt="">
        <img src="warning.png" alt="Warning sign">
    </body>
</html>
"""

issues = check_informative_images(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Informative image with missing or empty alt",
        "type": "Screen Reader",
        "severity": "High",
        "description": "The image 'informative.png' (informative) has no or empty alt. Screen reader users won't perceive the information.",
        "remediation": "Add a short, meaningful alt text that conveys the message.",
        "wcag_reference": "1.1.1",
        "impact": "Essential information is lost for screen reader users.",
        "page_url": "https://example.com",
        "resolution": "check_informative_images.md"
    },
    {
        "title": "Informative image has a generic alt text",
        "type": "Screen Reader",
        "severity": "Medium",
        "description": "The image 'warning.png' uses a generic alt 'Warning sign', which doesn't fully describe the image content.",
        "remediation": "Use a short phrase describing the specific meaning of the image.",
        "wcag_reference": "1.1.1",
        "impact": "Screen reader users receive a non-informative label instead of actual content.",
        "page_url": "https://example.com",
        "resolution": "check_informative_images.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Identifies missing, empty, or generic alt attributes for informative images.
3️⃣ OCR Comparison: If the image exists in the downloaded_images/ folder, extracts text using Tesseract OCR and compares it to the alt text.
4️⃣ Flags mismatches between extracted text and alt text based on a 30% similarity threshold.
5️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<img src="informative.png" alt="">
<img src="warning.png" alt="image">
✅ Corrected:

html
Copy
Edit
<img src="informative.png" alt="Step-by-step guide on how to assemble the product.">
<img src="warning.png" alt="Triangle warning sign indicating a hazard.">
📚 WCAG Reference
Success Criterion 1.1.1 - Non-text Content
→ Ensure that all informative images have meaningful alt attributes to provide accessibility for screen readers.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation
📖 Tesseract OCR Documentation