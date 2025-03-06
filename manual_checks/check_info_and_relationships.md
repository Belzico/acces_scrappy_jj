# 📑 Info and Relationships Tester - `check_info_and_relationships.py`

This script detects **structural and semantic issues in web content**, ensuring that information and relationships between elements are correctly conveyed.  
It follows **WCAG 1.3.1 (Info and Relationships, Level A)** to improve accessibility for screen reader users and assistive technologies.

## 📌 Why is this important?
Users who rely on assistive technologies need **proper semantic structure** in web pages to navigate and understand the content effectively.  
If elements are not correctly labeled or structured, the following issues may occur:

- ❌ **Screen readers may not interpret the structure correctly.**
- ❌ **Users may struggle to understand relationships between elements.**
- ❌ **Navigation may become confusing, affecting usability and accessibility.**

---

## ⚠️ **Detected Issues**
The script scans and reports the following accessibility problems:

### 1️⃣ **Missing semantic headings**
   - **Detects pages without any `<h1>` to `<h6>` headings.**
   - **Incorrect example:**  
   ```html
   <div class="title">Page Title</div>
Solution:
html
Copy
Edit
<h1>Page Title</h1>
2️⃣ Tables without proper <th> headers or relationships
Detects tables using role="presentation" while containing <th> elements.
Incorrect example:
html
Copy
Edit
<table role="presentation">
    <tr><th>Header</th></tr>
</table>
Solution:
html
Copy
Edit
<table>
    <tr><th scope="col">Header</th></tr>
</table>
Detects <th> elements missing scope or headers attributes.
Incorrect example:
html
Copy
Edit
<th>Header</th>
Solution:
html
Copy
Edit
<th scope="col">Header</th>
3️⃣ Form fields missing labels or ARIA attributes
Detects form fields without an associated <label> or ARIA attributes.
Incorrect example:
html
Copy
Edit
<input type="text" id="username">
Solution:
html
Copy
Edit
<label for="username">Username:</label>
<input type="text" id="username">
4️⃣ Radio and checkbox groups missing <fieldset> and <legend>
Detects groups of radio buttons or checkboxes that are not enclosed in a <fieldset> with a <legend>.
Incorrect example:
html
Copy
Edit
<input type="radio" name="gender" value="male"> Male
<input type="radio" name="gender" value="female"> Female
Solution:
html
Copy
Edit
<fieldset>
    <legend>Select your gender:</legend>
    <input type="radio" name="gender" value="male"> Male
    <input type="radio" name="gender" value="female"> Female
</fieldset>
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
from check_info_and_relationships import check_info_and_relationships

with open("test_info_and_relationships.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///path/to/test_info_and_relationships.html"
incidences = check_info_and_relationships(html_content, page_url)

for inc in incidences:
    print(inc)
📄 Example of a Detected Issue
If a table contains <th> elements but lacks scope or headers, the tester will generate the following report:

json
Copy
Edit
{
    "title": "Table header <th> missing 'scope' and 'headers'",
    "type": "Table Structure",
    "severity": "Medium",
    "description": "A <th> element does not specify 'scope' or is not associated with 'headers'.",
    "remediation": "Add scope='col' or scope='row', or associate with headers/id.",
    "wcag_reference": "1.3.1",
    "impact": "Screen reader users may not understand the relationship between table cells.",
    "page_url": "file:///path/to/test_info_and_relationships.html",
    "resolution": "check_info_and_relationships.md",
    "element_info": {
        "tag": "th",
        "id": "N/A",
        "class": "table-header",
        "line_number": 20
    }
}
✅ Benefits of Using This Tester
✔ Detects missing semantic structure in web pages.
✔ Ensures compliance with WCAG 1.3.1 for better content relationships.
✔ Improves accessibility for screen readers and assistive technologies.
✔ Easy integration with global_tester.py for batch analysis.

💡 With this tester, we ensure that web content is structured properly for all users! 🚀