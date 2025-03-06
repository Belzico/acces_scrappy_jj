# 🛑 Form Error Identification Tester - `check_form_error_identification.py`

This script detects **form fields that are marked as invalid (`aria-invalid="true"`) but lack a visible error message**.  
It ensures that users receive **clear and accessible feedback** about form errors, in compliance with **WCAG 3.3.1 (Error Identification, Level A).**

## 📌 Why is this important?
When a form field is invalid, users **must be provided with clear error messages** that describe the issue and how to fix it.  
If an error message is not properly linked to the field or is hidden, users—especially those using assistive technologies—may face the following problems:

- ❌ **Not knowing what is wrong with their input.**
- ❌ **Struggling to navigate forms due to missing feedback.**
- ❌ **Being unable to complete forms successfully.**

---

## ⚠️ **Detected Issues**
The script scans and reports the following accessibility problems:

### 1️⃣ **Form fields without an error message**
   - **Detects fields marked as `aria-invalid="true"` but without an associated error message.**
   - **Incorrect example:**  
   ```html
   <input type="text" name="email" aria-invalid="true">
Solution:
html
Copy
Edit
<input type="text" name="email" aria-invalid="true" aria-describedby="email-error">
<span id="email-error">Please enter a valid email.</span>
2️⃣ Form fields with aria-describedby pointing to hidden error messages
Detects fields where the referenced error message (aria-describedby) is hidden using display: none or similar styles.
Incorrect example:
html
Copy
Edit
<input type="text" name="email" aria-invalid="true" aria-describedby="email-error">
<span id="email-error" style="display: none;">Invalid email.</span>
Solution:
html
Copy
Edit
<span id="email-error">Invalid email.</span>
3️⃣ Error messages not linked via aria-describedby
Detects error messages present in the HTML but not programmatically linked to the field.
Incorrect example:
html
Copy
Edit
<input type="text" name="email" aria-invalid="true">
<p class="error-text">Invalid email format.</p>
Solution:
html
Copy
Edit
<input type="text" name="email" aria-invalid="true" aria-describedby="email-error">
<p id="email-error" class="error-text">Invalid email format.</p>
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
from check_form_error_identification import check_form_error_identification

with open("test_form_error.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///path/to/test_form_error.html"
incidences = check_form_error_identification(html_content, page_url)

for inc in incidences:
    print(inc)
📄 Example of a Detected Issue
If an invalid form field lacks a visible error message, the tester will generate the following report:

json
Copy
Edit
{
    "title": "Form field missing visible error message",
    "type": "Error Identification",
    "severity": "High",
    "description": "The field 'email' is marked as invalid but lacks a visible error message.",
    "remediation": "Ensure a visible text error message is present near the field or linked via aria-describedby.",
    "wcag_reference": "3.3.1",
    "impact": "Users may not understand what error needs correction.",
    "page_url": "file:///path/to/test_form_error.html",
    "resolution": "check_form_error_identification.md",
    "element_info": {
        "tag": "input",
        "id": "email-field",
        "name": "email"
    }
}
✅ Benefits of Using This Tester
✔ Detects form fields with missing or hidden error messages.
✔ Ensures compliance with WCAG 3.3.1 for better user feedback.
✔ Improves accessibility for screen readers and assistive technologies.
✔ Easy integration with global_tester.py for batch analysis.

💡 With this tester, we ensure that form errors are clearly communicated to all users! 🚀