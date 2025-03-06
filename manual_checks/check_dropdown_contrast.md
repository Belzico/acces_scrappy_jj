# 🎨 Dropdown Contrast Accessibility Checker - `check_dropdown_contrast.py`

This script checks whether the selected values in dropdown menus (i.e., `<select>` elements) have **sufficient color contrast** according to WCAG **1.4.3 (Contrast Minimum, Level AA)**.

## 📌 Why is this important?
Low-contrast text in dropdown menus can make it difficult for users with **low vision** or **color blindness** to read the selected value.

### ❌ **Incorrect Example (Fails Contrast)**
```html
<select>
    <option selected style="color: #BAC7CB; background-color: #FFFFFF;">Option 1</option>
</select>
👀 The text color #BAC7CB does not contrast enough with the white background #FFFFFF.

✅ Correct Example (Passes Contrast)
html
Copy
Edit
<select>
    <option selected style="color: #2C3E50; background-color: #FFFFFF;">Option 1</option>
</select>
✔ The text color #2C3E50 improves readability.

🛠️ How the Tester Works
Extracts all <select> elements from the page.
Finds the selected option (<option selected>).
If no option is explicitly selected, it defaults to the first visible <option>.
Checks text and background colors (from inline styles or defaults).
Calculates the contrast ratio.
If the contrast is below 4.5:1, the script generates an accessibility issue.
🚀 How to Use the Tester
📌 Installation
Ensure BeautifulSoup is installed:

sh
Copy
Edit
pip install beautifulsoup4
📌 Run the Tester in an HTML File
python
Copy
Edit
from check_dropdown_contrast import check_dropdown_contrast

with open("test_dropdown.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///path/to/test_dropdown.html"
issues = check_dropdown_contrast(html_content, page_url)

for issue in issues:
    print(issue)
📄 Example of a Detected Issue
If a dropdown has poor contrast, the tester will report:

json
Copy
Edit
{
    "title": "Dropdown selected value fails contrast once expanded",
    "type": "Color Contrast",
    "severity": "High",
    "description": "The selected option in the dropdown has a contrast ratio of 3.2:1, which does not meet the minimum recommended contrast ratio of 4.5:1 for small text.",
    "remediation": "Use a darker text color or change the background to increase contrast. Example: `color: #2C3E50;` instead of `color: #BAC7CB;`.",
    "wcag_reference": "1.4.3",
    "impact": "Users with low vision may not be able to read the selected dropdown text.",
    "page_url": "file:///path/to/test_dropdown.html",
    "affected_element": "<option selected style='color: #BAC7CB; background-color: #FFFFFF;'>Option 1</option>"
}
✅ Why Use This Tester?
✔ Detects low-contrast text in dropdown menus.
✔ Helps ensure WCAG compliance for color contrast (1.4.3).
✔ Automatically generates reports for accessibility audits.
✔ Easy integration with other accessibility checkers.

📢 Make your website accessible for all users! 🚀