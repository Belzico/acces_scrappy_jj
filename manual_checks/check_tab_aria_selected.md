# 🏷️ Check for Missing `aria-selected` in Tabs  

## 📌 Overview  
This script detects accessibility issues related to **tabs missing the `aria-selected="true"` attribute**.  
Ensuring that **the active tab is properly announced** helps screen readers provide accurate navigation for users relying on assistive technology.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Tabs (`role="tab"`) missing `aria-selected="true"`**, making it unclear which tab is active.  
- **Ensuring at least one tab is marked as selected.**  
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
from check_tab_aria_selected import check_tab_aria_selected

html_content = """
<html>
    <body>
        <div role="tablist">
            <button role="tab">Tab 1</button>
            <button role="tab">Tab 2</button>
        </div>
    </body>
</html>
"""

issues = check_tab_aria_selected(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Selected tab state is not announced",
        "type": "Screen Reader",
        "severity": "Medium",
        "description": "None of the tabs on the page have the attribute `aria-selected=\"true\"`. This means that screen reader users will not be able to identify which tab is active.",
        "remediation": "Add `aria-selected=\"true\"` to the active tab within a `role=\"tablist\"`. Example: `<button role=\"tab\" aria-selected=\"true\">My Groupons</button>`.",
        "wcag_reference": "4.1.2",
        "impact": "Screen reader users may not know which tab is currently selected.",
        "page_url": "https://example.com",
        "resolution": "check_tab_aria_selected.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all elements with role="tab".
3️⃣ Checks if at least one tab has aria-selected="true".
4️⃣ If missing, flags an issue with severity, impact, and remediation.
5️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<div role="tablist">
    <button role="tab">Tab 1</button>
    <button role="tab">Tab 2</button>
</div>
✅ Corrected:

html
Copy
Edit
<div role="tablist">
    <button role="tab" aria-selected="true">Tab 1</button>
    <button role="tab" aria-selected="false">Tab 2</button>
</div>
📚 WCAG Reference
Success Criterion 4.1.2 - Name, Role, Value
→ Ensure that interactive components provide the correct roles, states, and properties for assistive technologies.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation