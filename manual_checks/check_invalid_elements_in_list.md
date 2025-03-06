📋 Check Invalid Elements in Lists (check_invalid_elements_in_list.py)
This script checks for invalid elements (<div>) inside <ul> or <ol> lists that could cause HTML validation issues and accessibility concerns.

🚀 Overview
✅ What does it check?
Finds all <ul> and <ol> elements in the HTML.
Detects <div> elements directly inside these lists, which is not valid HTML.
Generates an issue if a <div> is found instead of a proper <li>.
❌ Why is this an issue?
HTML validation errors: <ul> and <ol> should contain only <li>, <script>, or <template> elements.
Assistive technology compatibility: Screen readers may misinterpret list content if invalid elements are used.
📌 Example of an Invalid List ❌
html
Copy
Edit
<ul>
    <li>Item 1</li>
    <div>Item 2</div> <!-- ❌ This should be inside <li> -->
    <li>Item 3</li>
</ul>
✔ Corrected version:

html
Copy
Edit
<ul>
    <li>Item 1</li>
    <li><div>Item 2</div></li> <!-- ✅ Wrapped inside <li> -->
    <li>Item 3</li>
</ul>
🔧 Installation
Clone the repository:

sh
Copy
Edit
git clone https://github.com/your-repo/accessibility-checker.git
cd accessibility-checker
Install dependencies:

sh
Copy
Edit
pip install -r requirements.txt
🖥️ Usage
To run the script manually:

sh
Copy
Edit
python check_invalid_elements_in_list.py "example.html"
Or as part of a larger accessibility testing suite.

🛠️ Function Usage
You can use the function inside a Python script:

python
Copy
Edit
from check_invalid_elements_in_list import check_invalid_elements_in_list

with open("example.html", "r", encoding="utf-8") as file:
    html_content = file.read()

issues = check_invalid_elements_in_list(html_content, "https://example.com")
print(issues)
📂 Output Format
The script returns a list of detected issues.
Each issue follows this structure:

json
Copy
Edit
{
    "title": "Div elements nested inside ul/ol in the navigation menu",
    "type": "HTML Validator",
    "severity": "Low",
    "description": "A `<ul>` or `<ol>` element should not contain `<div>` elements as direct children...",
    "remediation": "Ensure that `<div>` elements inside `<ul>` or `<ol>` are wrapped in `<li>`...",
    "wcag_reference": "4.1.1",
    "impact": "No immediate impact, but it may cause validation issues and future compatibility problems.",
    "page_url": "https://example.com",
    "resolution": "check_invalid_elements_in_list.md",
    "element_info": {
        "tag": "div",
        "text": "Menu Item",
        "id": "N/A",
        "class": "menu-item",
        "line_number": 23
    }
}
Additionally, issues are exported to an Excel file (issue_report.xlsx).

📖 WCAG Reference
WCAG 2.1 - 4.1.1 Parsing
"Ensure that elements are nested correctly and follow proper HTML structure for better accessibility support."
🔗 Read more on WCAG Parsing Guidelines

🏆 Why Use This?
✅ Ensures proper HTML validation
✅ Improves accessibility for assistive technologies
✅ Prevents unexpected behavior in web navigation menus
✅ Automatic Excel reporting for issue tracking

📢 Contribute
Found an issue or want to improve this script? Feel free to submit a pull request or open an issue in the repository. 🚀