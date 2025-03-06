🆔 Check for Duplicate ID Attributes
📌 Overview
This script detects duplicate id attributes in an HTML document, which can cause accessibility issues and unexpected behavior in assistive technologies. Each id must be unique in the DOM to ensure proper functionality.

✅ What It Does
Scans the HTML for all elements with an id attribute.
Identifies duplicate id values used in multiple elements.
Generates a detailed report listing:
The duplicated id.
The HTML tags where it appears.
Potential impact on users.
A suggested remediation to fix the issue.
Exports the findings to Excel (issue_report.xlsx).
🚀 Installation
Make sure you have the required dependencies installed:

sh
Copy
Edit
pip install beautifulsoup4 openpyxl
🖥️ Usage
To run the script, provide an HTML string and a page URL:

python
Copy
Edit
from check_duplicate_ids import check_duplicate_ids

html_content = """
<html>
    <body>
        <div id="menu">Main Menu</div>
        <span id="menu">Duplicate ID</span>
    </body>
</html>
"""

issues = check_duplicate_ids(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Duplicated id in fields",
        "type": "HTML Validator",
        "severity": "High",
        "description": "The id `menu` is used multiple times in 2 different elements (div, span). This can cause issues with assistive technologies and web scripts. Each `id` must be unique within the DOM.",
        "remediation": "Ensure that each `id` in the page is unique. If multiple instances are needed, use `class` instead or add a unique suffix, e.g., `id='menu_1'`.",
        "wcag_reference": "4.1.1",
        "impact": "Users relying on assistive technologies may not receive the correct content.",
        "page_url": "https://example.com",
        "resolution": "check_duplicate_ids.md",
        "element_info": "['div', 'span']//////menu"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Finds all elements with an id attribute.
3️⃣ Identifies duplicate id values and lists the affected elements.
4️⃣ Creates a structured report with severity, impact, and remediation.
5️⃣ Exports the results to Excel for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:
html
Copy
Edit
<div id="menu">Main Menu</div>
<span id="menu">Duplicate ID</span>
✅ Corrected:
html
Copy
Edit
<div id="menu">Main Menu</div>
<span id="menu_1">Unique ID</span>
Alternative Fix: Use class instead of id when multiple elements share the same styling or behavior.

📚 WCAG Reference
Success Criterion 4.1.1 - Parsing
→ Ensure elements have unique attributes to prevent errors in assistive technologies.
🔗 More Info
📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!
🔗 References
🌍 WCAG 2.1 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation