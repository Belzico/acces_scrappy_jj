# 🔍 ARIA Label Misuse in `<div>` Elements - `check_aria_label_in_div.py`

This tester detects **`<div>` elements that use `aria-label` without a valid `role` attribute**.  
ARIA attributes should only be used in elements that support them.  
If a `<div>` has an `aria-label` but lacks a `role`, it might cause **accessibility issues** for screen readers.

## 📌 Why is this important?

The **WCAG 4.1.2 (Name, Role, Value)** guideline states that elements **must have appropriate roles and attributes** for assistive technologies to understand them properly.  

### ❌ **Incorrect Example**
```html
<div aria-label="Main Menu">
    <ul>
        <li>Home</li>
        <li>About</li>
    </ul>
</div>
✅ Corrected Version

html
Copy
Edit
<nav aria-label="Main Menu">
    <ul>
        <li>Home</li>
        <li>About</li>
    </ul>
</nav>
Or:

html
Copy
Edit
<div role="navigation" aria-label="Main Menu">
    <ul>
        <li>Home</li>
        <li>About</li>
    </ul>
</div>
⚠️ Problem Detected
This script identifies <div> elements with an aria-label but missing a valid role.

📄 Example of a Reported Issue
json
Copy
Edit
{
    "title": "ARIA label used in <div> without a role",
    "type": "HTML Validator",
    "severity": "Low",
    "description": "The `aria-label` attribute should only be used on elements that support it. "
                   "Currently, it is applied to a `<div>` without a defined `role`, which is not valid.",
    "remediation": "Ensure that `<div>` elements with `aria-label` have an appropriate `role`, such as `role=\"button\"`, `role=\"option\"`, etc. "
                   "If `aria-label` is not necessary, consider using a `<span>` or `<button>` instead.",
    "wcag_reference": "4.1.2",
    "impact": "No immediate impact, but it may cause issues in validators and assistive technologies.",
    "page_url": "https://example.com",
    "resolution": "check_aria_label_in_div.md",
    "element_info": {
        "tag": "div",
        "text": "Main Menu",
        "id": "N/A",
        "class": "menu-container",
        "line_number": 45
    }
}
🚀 How to Use the Tester
📌 Installation
Ensure you have the required dependencies installed:

sh
Copy
Edit
pip install beautifulsoup4 pandas
📌 Run the Tester
Import and execute the function in a Python script:

python
Copy
Edit
from check_aria_label_in_div import check_aria_label_in_div

with open("test_page.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "https://example.com"
incidences = check_aria_label_in_div(html_content, page_url)

for inc in incidences:
    print(inc)
📂 Saving Results to Excel
This tester automatically saves results to an Excel file called issue_report.xlsx.

✅ Benefits of this Tester
✔ Detects ARIA misuse in <div> elements.
✔ Suggests role replacements for better accessibility.
✔ Generates structured reports for accessibility validation.
✔ Helps ensure compliance with WCAG 4.1.2 guidelines.

💡 By using this tester, you improve accessibility and assistive technology compatibility. 🚀