# 🏷️ Name, Role, and Value Accessibility Tester - `check_name_role_value.py`

This script detects **UI components that lack an accessible name, role, or value**, ensuring compliance with **WCAG 4.1.2 (Name, Role, Value, Level A)**.

## 📌 Why is this important?
Assistive technologies rely on **name, role, and value attributes** to help users interact with elements on a webpage.  
If these attributes are missing, the following issues may arise:

- ❌ **Screen readers may not identify elements properly.**
- ❌ **Users may not understand the function of interactive components.**
- ❌ **Checkboxes and radio buttons may not announce their state.**

---

## ⚠️ **Detected Issues**
The script scans for **interactive elements without accessible attributes** and provides remediation suggestions.

### 1️⃣ **Elements missing an accessible name**
   - **Detects `<button>`, `<input>`, `<textarea>`, `<select>`, `<a>`, `<div>`, and `<span>` elements that lack `aria-label`, `aria-labelledby`, or textual content.**
   - **Incorrect example:**  
   ```html
   <button></button>
Solution:
html
Copy
Edit
<button aria-label="Submit form"></button>
2️⃣ Elements missing an accessible role
Detects <div> or <span> elements acting as interactive elements without a proper role attribute.
Incorrect example:
html
Copy
Edit
<div onclick="openMenu()">Open Menu</div>
Solution:
html
Copy
Edit
<div role="button" tabindex="0" onclick="openMenu()">Open Menu</div>
3️⃣ Checkboxes and radio buttons missing a programmatic value
Detects checkboxes and radio buttons without aria-checked or checked.
Incorrect example:
html
Copy
Edit
<input type="checkbox" id="subscribe">
Solution:
html
Copy
Edit
<input type="checkbox" id="subscribe" aria-checked="false">
🚀 How to Use the Tester
📌 Installation
Ensure you have BeautifulSoup installed:

bash
Copy
Edit
pip install beautifulsoup4
📌 Run the Tester on an HTML File
python
Copy
Edit
from check_name_role_value import check_name_role_value

with open("test_name_role_value.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///path/to/test_name_role_value.html"
incidences = check_name_role_value(html_content, page_url)

for inc in incidences:
    print(inc)
📄 Example of a Detected Issue
If a <button> element lacks an accessible name, the tester will generate the following report:

json
Copy
Edit
{
    "title": "Missing accessible name",
    "type": "Name, Role, Value",
    "severity": "High",
    "description": "The element 'button' with ID 'submit_btn' does not have an accessible name.",
    "remediation": "Add an 'aria-label', 'aria-labelledby', or provide textual content.",
    "wcag_reference": "4.1.2",
    "impact": "Screen reader users may not understand the purpose of this element.",
    "page_url": "file:///path/to/test_name_role_value.html",
    "resolution": "check_name_role_value.md",
    "element_info": {
        "tag": "button",
        "id": "submit_btn",
        "line_number": 35
    }
}
✅ Benefits of Using This Tester
✔ Detects elements that are inaccessible to screen readers.
✔ Ensures all interactive components have proper name, role, and value attributes.
✔ Improves compliance with WCAG 4.1.2 and assistive technology usability.
✔ Automatically generates an Excel report for issue tracking.

💡 With this tester, we ensure that all users can effectively interact with web elements! 🚀