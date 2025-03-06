# 🏷️ Check for Decorative Images Accessibility  

## 📌 Overview  
This script detects accessibility issues with decorative images and elements in an HTML document. It ensures that purely decorative images are correctly hidden from screen readers and keyboard focus, and that they do not have misleading attributes.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Images (`<img>`)** missing an `alt` attribute.  
- **Decorative images** that are still announced to screen readers.  
- **Decorative images with incorrect `alt` text** instead of an empty `alt=""`.  
- **Decorative elements (`<hr>`, `<svg>`)** that are incorrectly focusable or announced.  

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
from check_images_decorative import check_images_decorative

html_content = """
<html>
    <body>
        <img src="decorative.png">
        <img src="decorative.png" alt="">
        <hr>
    </body>
</html>
"""

issues = check_images_decorative(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Missing alt attribute",
        "type": "Screen Reader",
        "severity": "High",
        "description": "The image 'decorative.png' does not have an 'alt' attribute. All images must have an 'alt' attribute, either empty (alt=\"\") for decorative images or descriptive for informative images.",
        "remediation": "Ensure that all images have an 'alt' attribute. Use alt=\"\" for purely decorative images or provide a meaningful description.",
        "wcag_reference": "1.1.1",
        "impact": "Screen readers will announce 'image' without any description, confusing users.",
        "page_url": "https://example.com",
        "resolution": "check_images_decorative.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Scans for elements that should be hidden but are incorrectly exposed to screen readers.
3️⃣ Identifies missing alt attributes, incorrectly focusable decorative elements, and incorrect alt text usage.
4️⃣ Creates a structured report with severity, impact, and remediation.
5️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<img src="decorative.png">
<hr>
✅ Corrected:

html
Copy
Edit
<img src="decorative.png" alt="">
<hr aria-hidden="true">
📚 WCAG Reference
Success Criterion 1.1.1 - Non-text Content
→ Ensure that all decorative images are correctly hidden from assistive technologies.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation