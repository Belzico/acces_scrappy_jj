# 📌 Expandable Buttons Missing `aria-expanded` - `check_button_aria_expanded.py`

This script detects **expandable buttons that are missing the `aria-expanded` attribute**, which is essential for accessibility.  
Without `aria-expanded`, **screen readers cannot inform users whether a button expands or collapses content**.

---

## 📌 Why is this important?
According to the **Web Content Accessibility Guidelines (WCAG)**, elements that expand or collapse content **must inform users of their state**.  
If `aria-expanded` is missing, it causes issues such as:

- ❌ **Screen reader users will not know if content is expanded or collapsed.**
- ❌ **Keyboard users may struggle to navigate accordion-style menus.**
- ❌ **It can lead to confusion in interactive elements like dropdowns, sidebars, and accordions.**

---

## ⚠️ **Issue Detected**
The script identifies buttons (`<button>` elements and those with `role="button"`) that should control expandable content  
but **lack `aria-expanded="true"` or `aria-expanded="false"`**.

### ❌ **Incorrect Example (With Error)**
```html
<button class="menu-toggle">Menu</button> 
<!-- No aria-expanded attribute -->
✅ Correct Example (Fixed)
html
Copy
Edit
<button class="menu-toggle" aria-expanded="false">Menu</button> 
🚀 How to Use the Tester
📌 Installation
Ensure you have BeautifulSoup installed:

sh
Copy
Edit
pip install beautifulsoup4
📌 Run the Tester on an HTML File
python
Copy
Edit
from check_button_aria_expanded import check_button_aria_expanded

with open("test_page.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///path/to/test_page.html"
issues = check_button_aria_expanded(html_content, page_url)

for issue in issues:
    print(issue)
📄 Example of a Detected Issue
If an expandable button is missing aria-expanded, the tester will report:

json
Copy
Edit
{
    "title": "Expandable button missing aria-expanded",
    "type": "Screen Reader",
    "severity": "Medium",
    "description": "One or more expandable buttons do not have the `aria-expanded` attribute. "
                   "This means screen reader users will not know whether the button is expanded or collapsed.",
    "remediation": "Ensure that expandable buttons include `aria-expanded=\"true\"` or `aria-expanded=\"false\"`. "
                   "Example: `<button aria-expanded=\"false\">Categories</button>`.",
    "wcag_reference": "4.1.2",
    "impact": "Screen reader users may not receive correct information about the button state.",
    "page_url": "file:///path/to/test_page.html",
    "affected_elements": [
        "<button class='menu-toggle'>Menu</button>"
    ]
}
✅ Benefits of this Tester
✔ Detects missing aria-expanded attributes.
✔ Helps improve screen reader accessibility.
✔ Provides suggestions to fix the issues.
✔ Generates an Excel report for further analysis.

📌 With this tester, we ensure that expandable buttons provide proper accessibility feedback! 🚀