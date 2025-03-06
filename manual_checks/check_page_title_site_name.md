# 🏷️ Check for Missing Site Name in Page Title  

## 📌 Overview  
This script detects accessibility issues related to **the absence of the website name in the page title**.  
Ensuring that the **site name appears in the title** helps users recognize which website they are on, improving navigation and accessibility.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Missing site names in the `<title>` tag**, making it difficult for users to identify the website.  
- **Extracting the site name** from either `meta property="og:site_name"` or the domain name.  
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
from check_page_title_site_name_auto_minimal import check_page_title_site_name_auto_minimal

html_content = """
<html>
    <head>
        <meta property="og:site_name" content="ExampleSite">
        <title>Help Center</title>
    </head>
    <body>
        <h1>Welcome to the Help Center</h1>
    </body>
</html>
"""

issues = check_page_title_site_name_auto_minimal(html_content, "https://examplesite.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Page title does not contain site name",
        "type": "Other A11y",
        "severity": "Medium",
        "description": "The page title 'Help Center' does not include the site name 'ExampleSite'. This makes it harder for users to identify the website.",
        "remediation": "Update the <title> to include the site name. Example: 'Help Center - ExampleSite'.",
        "wcag_reference": "2.4.2",
        "impact": "Users may not easily recognize which site they are visiting.",
        "page_url": "https://examplesite.com",
        "resolution": "check_page_title_site_name_auto_minimal.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts the site name from meta property="og:site_name".
3️⃣ If no og:site_name is found, derives the site name from the domain.
4️⃣ Checks if the site name appears in the <title>.
5️⃣ If missing, flags an issue with severity, impact, and remediation.
6️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<title>Help Center</title>
✅ Corrected:

html
Copy
Edit
<title>Help Center - ExampleSite</title>
📚 WCAG Reference
Success Criterion 2.4.2 - Page Titled
→ Ensure that pages have descriptive and informative titles, including the site name when appropriate.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation