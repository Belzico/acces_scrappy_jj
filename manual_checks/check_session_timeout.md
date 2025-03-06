# 🏷️ Check for Session Timeout Accessibility  

## 📌 Overview  
This script detects accessibility issues related to **session timeouts** in an HTML document. It ensures that users are properly notified before being logged out and that screen readers announce the warning in a timely manner, in accordance with WCAG guidelines.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Missing session timeout warnings (`.session-warning`, `.timeout-alert`, `.modal-warning`).**  
- **Warnings that do not use `aria-live="assertive"`, preventing screen reader users from receiving immediate notifications.**  
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
from check_session_timeout import check_session_timeout

html_content = """
<html>
    <body>
        <div class="modal-warning">Your session will expire in 1 minute.</div>
    </body>
</html>
"""

issues = check_session_timeout(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "No session timeout warning",
        "type": "Screen Reader",
        "severity": "High",
        "description": "No session timeout warning message was detected before expiration. Screen reader users may be logged out without prior notice.",
        "remediation": "Implement a warning modal before session expiration with `aria-live='assertive'` so that users are properly notified.",
        "wcag_reference": "2.2.1",
        "impact": "Users may be locked out without knowing they have been logged out.",
        "page_url": "https://example.com",
        "resolution": "check_session_timeout.md"
    },
    {
        "title": "Session timeout warning is not screen reader friendly",
        "type": "Screen Reader",
        "severity": "Medium",
        "description": "A session timeout warning was detected, but it does not use `aria-live='assertive'`, which prevents it from being immediately announced to screen reader users.",
        "remediation": "Add `aria-live='assertive'` to the warning modal or alert.",
        "wcag_reference": "2.2.1",
        "impact": "Users with disabilities will not be notified in time about session expiration.",
        "page_url": "https://example.com",
        "resolution": "check_session_timeout.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all session timeout warning elements (.session-warning, .timeout-alert, .modal-warning).
3️⃣ Checks if a session timeout warning is missing.
4️⃣ Verifies if aria-live="assertive" is used to notify screen reader users.
5️⃣ If a session timeout warning is missing or improperly implemented, an issue is flagged.
6️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<div class="session-warning">Your session will expire soon.</div>
✅ Corrected:

html
Copy
Edit
<div class="session-warning" role="alert" aria-live="assertive">
    Your session will expire in 1 minute. Click here to extend your session.
</div>
📚 WCAG Reference
Success Criterion 2.2.1 - Timing Adjustable
→ Ensure that users are given adequate time and clear warnings before session expiration.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation