# 🏷️ Check for Informative Icons Accessibility  

## 📌 Overview  
This script detects accessibility issues with informative icons, images, and SVGs in an HTML document. It ensures that visual elements that convey information are correctly announced to screen readers by verifying the presence of appropriate accessibility attributes.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **CSS icons (`<span>`, `<i>`)** missing `aria-label` or hidden supporting text.  
- **Informative images (`<img>`)** without an `alt` attribute.  
- **SVGs** missing a `<title>` or `aria-labelledby`.  

It generates a detailed report listing:  
- The affected element and its attributes.  
- The severity of the issue.  
- The WCAG reference for accessibility compliance.  
- Suggested remediation steps.  
- **Exports the findings to Excel (`issue_report.xlsx`).**  

## 🚀 Installation  
Make sure you have the required dependencies installed:  

```sh
pip install beautifulsoup4 openpyxl
🖥️ Usage
To run the script, provide an HTML string and a page URL:

python
Copy
Edit
from check_icons_informative import check_icons_informative

html_content = """
<html>
    <body>
        <span class="icon"></span>
        <img src="warning.png">
        <svg><path d="M10 10 H 90 V 90 H 10 Z" /></svg>
    </body>
</html>
"""

issues = check_icons_informative(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Informative icon is not announced",
        "type": "Screen Reader",
        "severity": "High",
        "description": "An informative icon is present but does not provide an accessible label.",
        "remediation": "Ensure that icons conveying information are announced by screen readers by using `aria-label`, `aria-labelledby`, or adding visually hidden supporting text.",
        "wcag_reference": "1.1.1",
        "impact": "Screen reader users will not perceive the information conveyed by the icon.",
        "page_url": "https://example.com",
        "resolution": "check_icons_informative.md",
        "element_info": {
            "tag": "span",
            "text": "",
            "id": "N/A",
            "class": "icon",
            "line_number": "N/A"
        }
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Scans for elements that convey information visually but lack accessibility attributes.
3️⃣ Identifies missing labels (aria-label, alt, <title>).
4️⃣ Creates a structured report with severity, impact, and remediation.
5️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<span class="icon"></span>
<img src="warning.png">
<svg><path d="M10 10 H 90 V 90 H 10 Z" /></svg>
✅ Corrected:

html
Copy
Edit
<span class="icon" aria-label="Warning"></span>
<img src="warning.png" alt="Warning sign">
<svg aria-labelledby="svg-title"><title id="svg-title">Active event</title></svg>
📚 WCAG Reference
Success Criterion 1.1.1 - Non-text Content
→ Ensure that all informative images and icons have text alternatives for assistive technologies.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation