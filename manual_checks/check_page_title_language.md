# 🏷️ Check for Page Language Mismatch  

## 📌 Overview  
This script detects accessibility issues related to **content language inconsistencies**.  
Ensuring that **the primary language of the page matches the `<html lang="xx">` attribute** helps screen readers provide accurate pronunciation and enhances accessibility.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **A mismatch between the `<html lang="xx">` attribute and the detected language of the visible content.**  
- **Using `langid` to analyze individual text fragments.**  
- **Flagging pages where more than 20% of the content is in a different language than the defined one.**  
- **Exports the findings to Excel (`issue_report.xlsx`).**  

## 🚀 Installation  
Make sure you have the required dependencies installed:  

```sh
pip install beautifulsoup4 langid openpyxl
🖥️ Usage
To run the script, provide an HTML string and a page URL:

python
Copy
Edit
from check_page_title_language import check_page_title_language

html_content = """
<html lang="en">
    <head>
        <title>Example Page</title>
    </head>
    <body>
        <p>Welcome to our website!</p>
        <p>Bienvenido a nuestro sitio web.</p>
        <p>Willkommen auf unserer Webseite.</p>
    </body>
</html>
"""

issues = check_page_title_language(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Page language mismatch",
        "type": "Other A11y",
        "severity": "High",
        "description": "40.0% of the visible content on the page is in a language different from 'en' defined in <html lang>. Detected languages: {'en': 1, 'es': 1, 'de': 1}",
        "remediation": "Review the primary language of the content. If the page is in 'en', ensure that at least 80% of the visible content matches that language.",
        "wcag_reference": "3.1.1",
        "impact": "Users with screen readers may receive incorrect pronunciation if the content is in a different language than defined on the page.",
        "page_url": "https://example.com",
        "resolution": "check_page_title_language.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts the primary language from <html lang="xx">.
3️⃣ Extracts all visible text fragments from the page, excluding scripts, styles, and meta tags.
4️⃣ Uses langid to detect the language of each text fragment.
5️⃣ Calculates the percentage of content in different languages.
6️⃣ Flags an issue if more than 20% of the text is in a different language than expected.
7️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<html lang="en">
    <body>
        <p>Welcome to our website!</p>
        <p>Bienvenido a nuestro sitio web.</p>
    </body>
</html>
✅ Corrected:

html
Copy
Edit
<html lang="es">
    <body>
        <p>Bienvenido a nuestro sitio web.</p>
        <p>¡Esperamos que disfrute su visita!</p>
    </body>
</html>
OR, mark different language sections explicitly:

html
Copy
Edit
<html lang="en">
    <body>
        <p>Welcome to our website!</p>
        <p lang="es">Bienvenido a nuestro sitio web.</p>
    </body>
</html>
📚 WCAG Reference
Success Criterion 3.1.1 - Language of Page
→ Ensure that the primary language of the page is correctly identified to aid screen readers.

📊 Report Generation
This script automatically exports results to Excel (issue_report.xlsx), making it easy to review and track accessibility issues.

📢 Contributing
Found a bug? Open an issue or create a pull request.
Suggestions? Feel free to contribute to improve this tester!

🔗 References
🌍 WCAG 2.2 Guidelines
📖 HTML Specification
🏗 BeautifulSoup Documentation