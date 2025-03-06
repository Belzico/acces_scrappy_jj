# 🏷️ Check for Placeholder Text Contrast Issues  

## 📌 Overview  
This script detects accessibility issues related to **low contrast between placeholder text and the input background**.  
Ensuring that **placeholder text meets the required contrast ratio** helps users with low vision read form hints more easily.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Placeholder text in `<input>` fields that has insufficient contrast against its background.**  
- **Extracting text and background colors from inline `style` attributes.**  
- **Checking if the contrast ratio is below 4.5:1, the minimum for small text.**  
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
from check_placeholder_contrast import check_placeholder_contrast

html_content = """
<html>
    <body>
        <input type="text" placeholder="Enter your name" style="color: #BFCAD1; background-color: #FFFFFF;">
    </body>
</html>
"""

issues = check_placeholder_contrast(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Grey placeholder fails contrast on white background",
        "type": "Color Contrast",
        "severity": "High",
        "description": "The placeholder text in the input field has a contrast ratio of 2.5:1, which does not meet the minimum 4.5:1 requirement for small text.",
        "remediation": "Use a darker color for the placeholder text or change the background to improve contrast. Example: `color: #757575;` instead of `color: #BFCAD1;`.",
        "wcag_reference": "1.4.3",
        "impact": "Users with low vision may struggle to read the placeholder text.",
        "page_url": "https://example.com",
        "resolution": "check_placeholder_contrast.md",
        "affected_element": "<input type='text' placeholder='Enter your name' style='color: #BFCAD1; background-color: #FFFFFF;'>"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all <input> fields with a placeholder attribute.
3️⃣ Checks for inline style attributes defining text and background colors.
4️⃣ Calculates the contrast ratio between the placeholder text and the background.
5️⃣ Flags an issue if the contrast ratio is below 4.5:1 (the minimum for small text).
6️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<input type="text" placeholder="Enter your name" style="color: #BFCAD1; background-color: #FFFFFF;">
✅ Corrected:

html
Copy
Edit
<input type="text" placeholder="Enter your name" style="color: #757575; background-color: #FFFFFF;">
📚 WCAG Reference
Success Criterion 1.4.3 - Contrast (Minimum)
→ Ensure that text, including placeholder text, has sufficient contrast against its background.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation