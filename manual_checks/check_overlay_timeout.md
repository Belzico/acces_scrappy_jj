# 🏷️ Check for Overlay Timeout Accessibility  

## 📌 Overview  
This script detects accessibility issues related to **overlays that disappear too quickly** in an HTML document. It ensures that overlays remain visible long enough for users to read and interact with their content, in accordance with WCAG guidelines.  

## ✅ What It Does  
This tester scans an HTML document and identifies issues with:  
- **Overlays (`<div>`, `<dialog>`, `popup`, `modal`)** that disappear too quickly after being triggered.  
- **Buttons (`<button>`, `<a onclick>`, `<div onclick>`)** that activate overlays.  
- **Checks if overlays disappear in less than a specified duration (`min_duration`, default: 5 seconds).**  
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
from check_overlay_timeout import check_overlay_timeout

html_content = """
<html>
    <body>
        <button onclick="openOverlay()">Open Modal</button>
        <div id="example-overlay" class="modal" style="display: none;"></div>
    </body>
</html>
"""

issues = check_overlay_timeout(html_content, "https://example.com")
print(issues)
🔍 Example Output
json
Copy
Edit
[
    {
        "title": "Overlay disappears too quickly",
        "type": "Other A11y",
        "severity": "High",
        "description": "The overlay 'example-overlay' automatically disappears in 3 seconds after clicking the button 'Open Modal'. This may prevent some users from properly interacting with it.",
        "remediation": "Ensure that the overlay remains visible until the user manually closes it, or provide an option in the settings to adjust the timing.",
        "wcag_reference": "2.2.1",
        "impact": "Users with visual, motor, or cognitive disabilities may not have enough time to read or interact with the overlay content before it disappears.",
        "page_url": "https://example.com",
        "resolution": "check_overlay_timeout.md"
    }
]
📂 How It Works
1️⃣ Parses the HTML using BeautifulSoup.
2️⃣ Extracts all buttons (<button>, <a onclick>, <div onclick>) that trigger overlays.
3️⃣ Identifies overlays (<div>, <dialog>, .overlay, .popup, .modal).
4️⃣ Checks if overlays disappear in less than the specified min_duration (default: 5s).
5️⃣ If an overlay disappears too quickly, an issue is flagged.
6️⃣ Exports the results to Excel (issue_report.xlsx) for further analysis.

🛠️ Fixing the Issue
❌ Incorrect:

html
Copy
Edit
<button onclick="openOverlay()">Open Modal</button>
<div id="example-overlay" class="modal" style="display: none;"></div>
<script>
    setTimeout(() => { document.getElementById('example-overlay').style.display = 'none'; }, 3000);
</script>
✅ Corrected:

html
Copy
Edit
<button onclick="openOverlay()">Open Modal</button>
<div id="example-overlay" class="modal">
    <p>Overlay content</p>
    <button onclick="closeOverlay()">Close</button>
</div>
<script>
    function closeOverlay() {
        document.getElementById('example-overlay').style.display = 'none';
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