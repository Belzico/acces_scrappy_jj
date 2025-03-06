📌 README: Check Alt Distinction Tester
🔍 Overview
The Check Alt Distinction tester analyzes <img> elements to identify missing, empty, or redundant alt attributes. It ensures compliance with WCAG 1.1.1 by detecting issues that affect screen reader users.

This script:

Detects missing alt attributes (high priority issue).
Flags empty alt="" attributes when images are inside links/buttons with no accessible text.
Uses semantic similarity analysis with Sentence Transformers to detect redundant alt text.
🛠 How It Works
The tester processes an HTML file and:

Identifies missing alt attributes, which cause screen readers to read filenames.
Detects decorative images (alt="") used incorrectly inside interactive elements without accessible labels.
Compares alt attributes with nearby text using semantic similarity analysis to avoid redundancy.
⚠️ Detected Issues
Issue	Description	WCAG	Severity
❌ Missing alt attribute	The image lacks an alt attribute, making its purpose unclear.	1.1.1	High
⚠ Link/Button with no accessible text	A decorative image inside a link/button has no text or aria-label, making it inaccessible.	1.1.1	High
⚠ Redundant alternative text	The alt text is semantically similar to nearby content, causing repetitive announcements for screen readers.	1.1.1	Medium
📌 Installation
Ensure dependencies are installed:

sh
Copy
Edit
pip install beautifulsoup4 sentence-transformers pandas
🚀 Usage
To run the tester on an HTML page:

python
Copy
Edit
from check_alt_distinction import check_alt_distinction

with open("sample.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "https://example.com"
incidences = check_alt_distinction(html_content, page_url)

for inc in incidences:
    print(inc)
🖥 Example Output
If an image is missing an alt attribute, the tester will return:

json
Copy
Edit
{
    "title": "Image missing alt attribute",
    "type": "Alternative Text",
    "severity": "High",
    "description": "This image does not have an alt attribute. Screen readers may announce the filename instead.",
    "remediation": "Add an appropriate alt attribute. If decorative, use `alt=''` and `aria-hidden='true'`. If informative, describe the image content in alt.",
    "wcag_reference": "1.1.1",
    "impact": "Screen reader users may not understand the image's purpose.",
    "page_url": "https://example.com",
    "resolution": "check_alt_distinction.md",
    "element_info": {
        "tag": "img",
        "id": "N/A",
        "class": "example-class",
        "line_number": 45
    }
}
📖 References
🏗 WCAG 1.1.1 - Non-Text Content
🏗 Sentence Transformers - Documentation
🏗 BeautifulSoup - Documentation
📢 Want to contribute? Feel free to open an issue or submit a pull request! 🚀