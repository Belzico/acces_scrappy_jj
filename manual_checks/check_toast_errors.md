# 🏷️ Check for Toast Error Message Accessibility  

## 📌 Overview  
This script detects accessibility issues related to **error messages that disappear too quickly** in an HTML document. It ensures that users have enough time to read and understand error messages before they disappear, in accordance with WCAG guidelines.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Toast messages (`<div class="toast">`, `<div class="notification">`, `<div class="error-message">`)** that disappear too quickly.  
- **Error messages that vanish in less than a specified duration (`min_duration`, default: 5 seconds).**  
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
from check_toast_errors import check_toast_errors

html_content = """
<html>
    <body>
        <div class="toast error-message">Invalid login credentials.</div>
    </body>
</html>
"""

issues = check_toast_errors(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Error message disappears too quickly",
        "type": "Other A11y",
        "severity": "High",
        "description": "The error message 'Invalid login credentials.' automatically disappears in 2 seconds. This may prevent some users from reading or understanding the error.",
        "remediation": "Ensure that error messages remain visible until the user manually dismisses them. Ideally, display the message near the form field causing the error.",
        "wcag_reference": "2.2.1",
        "impact": "Users may not notice the error and may not understand why the form was not submitted.",
        "page_url": "https://example.com",
        "resolution": "check_toast_errors.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all toast messages (.toast, .notification, .alert, .error-message).
3️⃣ Checks if error messages disappear in less than the specified min_duration (default: 5s).
4️⃣ If an error message disappears too quickly, an issue is flagged.
5️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<div class="toast error-message" style="animation: fadeOut 2s;">Invalid login credentials.</div>
✅ Corrected:

html
Copy
Edit
<div class="error-message" role="alert">
    Invalid login credentials. Please try again.
    <button onclick="closeMessage()">Dismiss</button>
</div>
<script>
    function closeMessage() {
        document.querySelector('.error-message').style.display = 'none';
    }
</script>
📚 WCAG Reference
Success Criterion 2.2.1 - Timing Adjustable
→ Ensure that users have enough time to interact with time-sensitive content.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation