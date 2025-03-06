# 🏷️ Check for Text Cutoff at 200% Zoom  

## 📌 Overview  
This script detects accessibility issues related to **text cutoff when zoomed to 200%** in an HTML document. It ensures that content remains visible and readable without being truncated or hidden, in accordance with WCAG guidelines.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Inline styles (`style="overflow: hidden;"`, `height`, `max-height`)** that may prevent text from expanding.  
- **CSS classes (`hidden`, `truncate`, `text-cutoff`)** that can lead to unintended text hiding.  
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
from check_zoom_text_cutoff import check_zoom_text_cutoff

html_content = """
<html>
    <head>
        <style>
            .truncate { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
        </style>
    </head>
    <body>
        <div style="height: 50px; overflow: hidden;">This text might be cut off.</div>
        <div class="truncate">This text might also be truncated.</div>
    </body>
</html>
"""

issues = check_zoom_text_cutoff(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Text may be cut off at 200% zoom",
        "type": "Zoom",
        "severity": "High",
        "description": "Elements with `overflow: hidden;`, `height`, or `max-height` detected, which may cause content to be hidden when zoomed to 200%.",
        "remediation": "Ensure that containers can dynamically expand when text size increases. Avoid `overflow: hidden;` in critical content sections and use `min-height` instead of `height`.",
        "wcag_reference": "1.4.4",
        "impact": "Users may lose access to important information when zooming.",
        "page_url": "https://example.com",
        "resolution": "check_zoom_text_cutoff.md"
    },
    {
        "title": "Text truncation detected",
        "type": "Zoom",
        "severity": "High",
        "description": "Classes `{'truncate'}` detected, which may truncate text and prevent visibility when zoomed to 200%.",
        "remediation": "Ensure that full content remains visible and accessible without requiring horizontal scrolling.",
        "wcag_reference": "1.4.4",
        "impact": "Text may be hidden without a way for users to access it.",
        "page_url": "https://example.com",
        "resolution": "check_zoom_text_cutoff.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all elements with inline styles that contain overflow: hidden;, height, or max-height.
3️⃣ Checks for common text-truncating CSS classes like hidden, truncate, text-cutoff.
4️⃣ If an issue is found, it is flagged with severity, impact, and remediation.
5️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<div style="height: 50px; overflow: hidden;">This text might be cut off.</div>
css
Copy
Edit
.truncate { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
✅ Corrected:

html
Copy
Edit
<div style="min-height: auto;">This text will adjust dynamically.</div>
css
Copy
Edit
.truncate { white-space: normal; overflow: visible; }
📚 WCAG Reference
Success Criterion 1.4.4 - Resize Text
→ Ensure that text can be resized up to 200% without loss of content or functionality.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation