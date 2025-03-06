# 🏷️ Check for Menu Text Spacing Issues  

## 📌 Overview  
This script detects accessibility issues related to **menu items being cut off or overflowing when text spacing adjustments are applied**, in accordance with WCAG guidelines. It ensures that users who increase line height, letter spacing, or word spacing can still access all menu content.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **`overflow: hidden;` in menu elements**, which may crop text when spacing increases.  
- **`white-space: nowrap;` in menus**, preventing text from wrapping properly.  
- **`max-height: Xpx;` applied to menus**, which may cause content to be cut off.  
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
from check_menu_text_spacing import check_menu_text_spacing

html_content = """
<html>
    <head>
        <style>
            .menu-item { overflow: hidden; white-space: nowrap; max-height: 40px; }
        </style>
    </head>
    <body>
        <nav>
            <ul class="menu">
                <li class="menu-item">This menu item might be cut off.</li>
            </ul>
        </nav>
    </body>
</html>
"""

issues = check_menu_text_spacing(html_content, "https://example.com")
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
        "description": "`overflow: hidden;` was detected in a menu item. This may cause content to be cut off when text spacing is increased.",
        "remediation": "Avoid using `overflow: hidden;` in menu items. Ensure that content expands properly.",
        "wcag_reference": "1.4.12",
        "impact": "Users who need additional spacing may not see the full content.",
        "page_url": "https://example.com",
        "resolution": "check_menu_text_spacing.md"
    },
    {
        "title": "Text does not wrap in the menu",
        "type": "Zoom",
        "severity": "High",
        "description": "`white-space: nowrap;` was detected, preventing text from wrapping properly when text spacing is increased.",
        "remediation": "Avoid using `white-space: nowrap;` in menus to allow text to adjust correctly.",
        "wcag_reference": "1.4.12",
        "impact": "Menu items may overflow from their container.",
        "page_url": "https://example.com",
        "resolution": "check_menu_text_spacing.md"
    },
    {
        "title": "Menu items may be cut off",
        "type": "Zoom",
        "severity": "High",
        "description": "`max-height` in pixels was detected in a menu, which may cause items to be cropped when text spacing increases.",
        "remediation": "Use `min-height: auto;` instead of fixed values to allow dynamic adjustment.",
        "wcag_reference": "1.4.12",
        "impact": "Users may not see the full content of the menu.",
        "page_url": "https://example.com",
        "resolution": "check_menu_text_spacing.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all navigation elements (<nav>, <ul>, <div> with menu-related classes).
3️⃣ Checks for overflow: hidden; in menu items, which can cause content to be cut off.
4️⃣ Detects white-space: nowrap; in menus, which prevents text from wrapping correctly.
5️⃣ Flags max-height: Xpx; applied to menus, which may cause text to be truncated.
6️⃣ If an issue is found, it is flagged with severity, impact, and remediation.
7️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<li style="overflow: hidden; white-space: nowrap; max-height: 40px;">This menu item might be cut off.</li>
css
Copy
Edit
.menu-item { overflow: hidden; white-space: nowrap; max-height: 40px; }
✅ Corrected:

html
Copy
Edit
<li style="overflow: visible; white-space: normal; min-height: auto;">This menu item adapts dynamically.</li>
css
Copy
Edit
.menu-item { overflow: visible; white-space: normal; min-height: auto; }
📚 WCAG Reference
Success Criterion 1.4.12 - Text Spacing
→ Ensure that menu items remain readable and accessible when spacing adjustments are applied.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation