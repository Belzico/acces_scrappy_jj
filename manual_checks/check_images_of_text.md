# 🏷️ Check for Images of Text Accessibility  

## 📌 Overview  
This script detects accessibility issues related to **images containing text** in an HTML document. It ensures that images with embedded text have an equivalent real text representation nearby, improving accessibility for screen readers and zoom users.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Images (`<img>`) that contain text** but lack an equivalent text alternative in the HTML.  
- **OCR (Optical Character Recognition) comparison** to check if the extracted text appears in the image’s `alt` attribute or nearby text.  
- **Exports the findings to Excel (`issue_report.xlsx`).**  

## 🚀 Installation  
Make sure you have the required dependencies installed:  

```sh
pip install beautifulsoup4 pytesseract pillow openpyxl
🔧 Additional Setup
You need to install Tesseract OCR to enable text extraction from images:

Windows: Download and install from Tesseract OCR.
Linux/macOS: Install via package manager (sudo apt install tesseract-ocr or brew install tesseract).
After installation, update the script’s pytesseract.pytesseract.tesseract_cmd path if necessary.

🖥️ Usage
To run the script, provide an HTML string and a page URL:

python
Copy
Edit
from check_images_of_text import check_images_of_text

html_content = """
<html>
    <body>
        <img src="text-image.png" alt="">
        <p>This is a caption.</p>
    </body>
</html>
"""

issues = check_images_of_text(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Image of Text Possibly Used",
        "type": "Screen Reader",
        "severity": "High",
        "description": "The image 'text-image.png' contains text (OCR detected): 'Warning: Slippery floor...' but there is no equivalent textual content in the HTML. This suggests an image of text without a real text alternative.",
        "remediation": "Use real HTML text instead of an image when possible. If an image is necessary, provide an alternative text version (Technique C30).",
        "wcag_reference": "1.4.5",
        "impact": "Users who rely on screen readers or zoom may struggle to access the text.",
        "page_url": "https://example.com",
        "resolution": "check_images_of_text.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all <img> elements and checks for a src attribute.
3️⃣ If the image file exists locally in downloaded_images/, it performs OCR to extract text from the image.
4️⃣ Compares the extracted text with the alt attribute and nearby text content to check if an alternative exists.
5️⃣ If no matching textual content is found, an issue is flagged.
6️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<img src="warning.png" alt="">
✅ Corrected:

html
Copy
Edit
<img src="warning.png" alt="Warning: Slippery floor.">
<p>Warning: Slippery floor.</p>
📚 WCAG Reference
Success Criterion 1.4.5 - Images of Text
→ Avoid using images of text unless essential. Provide a text-based alternative when possible.

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