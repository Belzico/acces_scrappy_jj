# 🎛 Accordion ARIA Expanded Check - `check_accordion_aria_expanded.py`

This script detects **accordion buttons that do not properly announce their state** using `aria-expanded`.  
If an accordion does not have `aria-expanded="true"` or `aria-expanded="false"`, screen reader users will not know whether the content is expanded or collapsed.

## 📌 Why is this important?
According to **WCAG 4.1.2 (Name, Role, Value)**, interactive elements must provide programmatic access to their state.  
Without `aria-expanded`, screen readers cannot announce whether an accordion section is open or closed, leading to:

- ❌ **Confusion for visually impaired users.**
- ❌ **Navigation issues when content is dynamically shown or hidden.**
- ❌ **Loss of accessibility compliance.**

---

## ⚠️ **Detected Issue**
This script scans the HTML for accordion buttons and verifies whether they have `aria-expanded` correctly set.

### ❌ **Incorrect Example (Fails Accessibility)**
```html
<button class="accordion-toggle">Section 1</button>
<button class="accordion-toggle" role="button">Section 2</button>
✅ Correct Example (Accessible)
html
Copy
Edit
<button class="accordion-toggle" aria-expanded="false">Section 1</button>
<button class="accordion-toggle" role="button" aria-expanded="true">Section 2</button>
🚀 How to Use the Tester
📌 Installation
Ensure BeautifulSoup and dependencies are installed:

sh
Copy
Edit
pip install beautifulsoup4 pandas openpyxl
📌 Running the Tester on an HTML File
python
Copy
Edit
from check_accordion_aria_expanded import check_accordion_aria_expanded

with open("test_accordion.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///path/to/test_accordion.html"
incidences = check_accordion_aria_expanded(html_content, page_url)

for inc in incidences:
    print(inc)
📄 Example of a Detected Issue
If an accordion button is missing aria-expanded, the tester will generate the following JSON report:

json
Copy
Edit
{
    "title": "Accordion items do not announce their state",
    "type": "Screen Reader",
    "severity": "Medium",
    "description": "One or more accordion buttons are missing the `aria-expanded` attribute. This prevents screen reader users from knowing whether the accordion is expanded or collapsed.",
    "remediation": "Add `aria-expanded=\"true\"` or `aria-expanded=\"false\"` to the accordion button. Example: `<button aria-expanded=\"false\">Section 1</button>`.",
    "wcag_reference": "4.1.2",
    "impact": "Screen reader users may not be aware of expandable content on the page.",
    "page_url": "file:///path/to/test_accordion.html",
    "resolution": "check_accordion_aria_expanded.md",
    "element_info": {
        "tag": "button",
        "text": "Section 1",
        "id": "N/A",
        "class": "accordion-toggle",
        "line_number": 12
    }
}
✅ Benefits of Using This Tester
✔ Detects missing aria-expanded attributes in accordions.
✔ Ensures compliance with WCAG 4.1.2.
✔ Provides detailed reports for debugging accessibility issues.
✔ Can be integrated into automated testing workflows.

📢 Contribute & Improve!
If you have suggestions or want to enhance this tester, feel free to open a Pull Request or report an Issue. 🚀