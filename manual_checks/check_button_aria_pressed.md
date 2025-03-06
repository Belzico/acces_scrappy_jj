# 🔘 Check Button ARIA Pressed - `check_button_aria_pressed.py`

This script **checks if buttons using `role="button"` announce their selected state** using the `aria-pressed="true"` attribute.

## 📌 Why is this important?
According to **WCAG 4.1.2**, interactive elements must properly convey their state to assistive technologies.  
If a visually selected button does **not** include `aria-pressed="true"`, **screen reader users may not know which button is active**.

---

## ⚠️ **Detected Issue**
The script searches for buttons (`role="button"`) and verifies if at least one includes `aria-pressed="true"`.  
If none are found, it reports an issue.

### ❌ **Incorrect Example (Issue Present)**
```html
<button role="button">Global Position</button>
❌ Problem: The button is visually selected, but screen readers won’t know it’s active.

✅ Correct Example (Fixed)
html
Copy
Edit
<button role="button" aria-pressed="true">Global Position</button>
✔ Solution: Adding aria-pressed="true" ensures screen readers announce the button as selected.

🚀 How to Use the Tester
📌 Installation
Ensure you have BeautifulSoup and the required dependencies installed:

sh
Copy
Edit
pip install beautifulsoup4 openpyxl
📌 Running the Tester
python
Copy
Edit
from check_button_aria_pressed import check_button_aria_pressed

with open("example.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///path/to/example.html"
incidences = check_button_aria_pressed(html_content, page_url)

for inc in incidences:
    print(inc)
📄 Example of a Detected Issue
If the script finds a missing aria-pressed="true", it reports:

json
Copy
Edit
{
    "title": "Selected button state is not announced",
    "type": "Screen Reader",
    "severity": "Medium",
    "description": "No buttons on the page have the `aria-pressed=\"true\"` attribute. "
                   "This means screen reader users will not know which button is currently selected.",
    "remediation": "Ensure that the selected button includes `aria-pressed=\"true\"`. "
                   "Example: `<button role=\"button\" aria-pressed=\"true\">Global Position</button>`.",
    "wcag_reference": "4.1.2",
    "impact": "Screen reader users may not be aware of which button is selected.",
    "page_url": "file:///path/to/example.html",
    "resolution": "check_button_aria_pressed.md",
    "affected_elements": [
        "<button role=\"button\">Global Position</button>"
    ]
}
✅ Benefits of This Tester
✔ Detects missing aria-pressed="true" in buttons.
✔ Ensures better accessibility for screen reader users.
✔ Exports detected issues to an Excel report (issue_report.xlsx).
✔ Easy integration into automated testing pipelines.

📢 Contribute & Improve
If you find improvements or want to contribute, submit a Pull Request! 🚀
For more WCAG guidelines, visit: Web Content Accessibility Guidelines.

💡 With this tester, we ensure all buttons are properly announced for assistive technologies! 🌍♿