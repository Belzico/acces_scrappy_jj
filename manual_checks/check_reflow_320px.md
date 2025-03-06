# 🏷️ Check for Reflow Issues at 320px  

## 📌 Overview  
This script detects accessibility issues related to **content reflow** when a webpage is viewed at **320px width**. It ensures that users do not need to scroll horizontally to access content, in accordance with WCAG guidelines.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Fixed-width elements (`style="width: 600px;"`)** that prevent proper content adaptation.  
- **CSS styles that set `width: Xpx` without `max-width: 100%`.**  
- **Forced horizontal scrolling (`overflow-x: scroll`).**  
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
from check_reflow_320px import check_reflow_320px

html_content = """
<html>
    <head>
        <style>
            .container { width: 800px; }
        </style>
    </head>
    <body>
        <div class="container">This is a test.</div>
    </body>
</html>
"""

issues = check_reflow_320px(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Fixed width elements detected (inline styles)",
        "type": "Zoom",
        "severity": "High",
        "description": "Elements with fixed pixel widths were found in `style` attributes, which may prevent content from adapting properly to a 320px viewport.",
        "remediation": "Replace fixed widths (`width: 600px;`) with flexible values (`max-width: 100%`, `flexbox`, `grid`).",
        "wcag_reference": "1.4.10",
        "impact": "Users must scroll horizontally to view content, making navigation difficult.",
        "page_url": "https://example.com",
        "resolution": "check_reflow_320px.md"
    },
    {
        "title": "Fixed width detected in CSS",
        "type": "Zoom",
        "severity": "High",
        "description": "A `width: Xpx` was detected in the page's CSS styles without `max-width`, which may prevent content from adapting properly to a 320px viewport.",
        "remediation": "Avoid `width: Xpx;` and use `max-width: 100%` or flexible CSS with `grid` or `flexbox`.",
        "wcag_reference": "1.4.10",
        "impact": "Users cannot view content without horizontal scrolling, which is a poor mobile practice.",
        "page_url": "https://example.com",
        "resolution": "check_reflow_320px.md"
    },
    {
        "title": "Horizontal scrolling detected",
        "type": "Zoom",
        "severity": "High",
        "description": "A horizontal scrollbar was detected on the page, indicating that the content does not properly adjust to a 320px viewport.",
        "remediation": "Modify containers to use `max-width: 100%` and avoid `overflow-x: scroll`.",
        "wcag_reference": "1.4.10",
        "impact": "Users cannot view content without horizontal scrolling, which is a poor mobile practice.",
        "page_url": "https://example.com",
        "resolution": "check_reflow_320px.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all elements with inline styles that contain width: Xpx but lack max-width.
3️⃣ Checks embedded CSS inside <style> tags for fixed widths without max-width.
4️⃣ Detects forced horizontal scrolling using overflow-x: auto or overflow-x: scroll.
5️⃣ If an issue is found, it is flagged with severity, impact, and remediation.
6️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<div style="width: 600px;">This text does not adapt.</div>
css
Copy
Edit
.container { width: 800px; }
✅ Corrected:

html
Copy
Edit
<div style="max-width: 100%;">This text adapts to the viewport.</div>
css
Copy
Edit
.container { max-width: 100%; display: flex; }
📚 WCAG Reference
Success Criterion 1.4.10 - Reflow
→ Ensure that content adapts properly to smaller screens without requiring horizontal scrolling.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation