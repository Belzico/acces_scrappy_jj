# 🏷️ Check for Missing `aria-expanded` in Expandable Buttons  

## 📌 Overview  
This script detects accessibility issues related to **expandable buttons missing the `aria-expanded` attribute**.  
Ensuring that **expandable buttons correctly indicate their state** helps screen reader users understand whether a section is expanded or collapsed.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Buttons (`<button>`, `role="button"`, or any element with `aria-expanded`) missing `aria-expanded="true"` or `aria-expanded="false"`.**  
- **Ensuring that expandable buttons provide state information for assistive technology users.**  
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
from check_mobile_button_aria_expanded import check_mobile_button_aria_expanded

html_content = """
<html>
    <body>
        <button>Menu</button>
        <div role="button">Expand Section</div>
    </body>
</html>
"""

issues = check_mobile_button_aria_expanded(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Button has no expanded/collapsed state announced on mobile",
        "type": "Screen Readers",
        "severity": "Medium",
        "description": "One or more expandable buttons are missing the `aria-expanded` attribute. This means that screen reader users on mobile devices will not know whether the button is expanded or collapsed.",
        "remediation": "Add `aria-expanded=\"true\"` or `aria-expanded=\"false\"` to the expandable button. Example: `<button aria-expanded=\"false\">See more</button>`.",
        "wcag_reference": "4.1.2",
        "impact": "Screen reader users on mobile devices will not receive information about the button's state.",
        "page_url": "https://example.com",
        "resolution": "check_mobile_button_aria_expanded.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all expandable buttons (<button>, role="button", or elements with aria-expanded).
3️⃣ Checks if at least one button has aria-expanded="true" or aria-expanded="false".
4️⃣ If missing, flags an issue with severity, impact, and remediation.
5️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<button>Menu</button>
<div role="button">Expand Section</div>
✅ Corrected:

html
Copy
Edit
<button aria-expanded="false">Menu</button>
<div role="button" aria-expanded="true">Expand Section</div>
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