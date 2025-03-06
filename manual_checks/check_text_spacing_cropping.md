# 🏷️ Check for Text Spacing and Cropping Issues  

## 📌 Overview  
This script detects accessibility issues related to **content cropping when text spacing adjustments are applied**, in accordance with WCAG guidelines. It ensures that users who increase line height, letter spacing, or word spacing do not lose access to content.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Containers using `overflow: hidden;`, `overflow-x: hidden;`, or `overflow-y: hidden;`**, which may cause text cropping.  
- **Fixed-height containers (`height: Xpx;`)**, which may prevent text from expanding properly when spacing increases.  
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
from check_text_spacing_cropping import check_text_spacing_cropping

html_content = """
<html>
    <head>
        <style>
            .text-box { height: 50px; overflow: hidden; }
        </style>
    </head>
    <body>
        <div class="text-box">This text might be cropped.</div>
    </body>
</html>
"""

issues = check_text_spacing_cropping(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Content may be cropped with text spacing adjustments",
        "type": "Zoom",
        "severity": "High",
        "description": "`overflow: hidden;` (or a variation -x/-y) was detected in a text container. This may cause content to be cut off when text spacing is increased.",
        "remediation": "Avoid using `overflow: hidden;` in text containers when applying additional spacing. Use `overflow: visible;` or allow dynamic expansion.",
        "wcag_reference": "1.4.12",
        "impact": "Users who need extra spacing may not see the full content.",
        "page_url": "https://example.com",
        "resolution": "check_text_spacing_cropping.md"
    },
    {
        "title": "Fixed height detected, may crop text",
        "type": "Zoom",
        "severity": "High",
        "description": "A fixed height in pixels (`height: XXXpx;`) was detected in a text container. This may prevent text from adjusting when extra spacing is applied.",
        "remediation": "Use `min-height: auto;` instead of fixed heights to allow dynamic expansion.",
        "wcag_reference": "1.4.12",
        "impact": "Text may be cut off when users increase spacing.",
        "page_url": "https://example.com",
        "resolution": "check_text_spacing_cropping.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all elements with inline styles that contain overflow: hidden;, overflow-x: hidden;, or overflow-y: hidden;.
3️⃣ Checks for fixed-height values (height: Xpx;) that may cause text cropping.
4️⃣ If an issue is found, it is flagged with severity, impact, and remediation.
5️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<div style="height: 50px; overflow: hidden;">This text might be cropped.</div>
css
Copy
Edit
.text-box { height: 60px; overflow: hidden; }
✅ Corrected:

html
Copy
Edit
<div style="min-height: auto; overflow: visible;">This text adjusts dynamically.</div>
css
Copy
Edit
.text-box { min-height: auto; overflow: visible; }
📚 WCAG Reference
Success Criterion 1.4.12 - Text Spacing
→ Ensure that text remains visible and readable when spacing adjustments are applied.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation