🎨 Buttons/Links Identified Only by Color - check_buttons_only_by_color.py
This script detects buttons and links that rely solely on color for identification, without additional visual cues like underlines, borders, or icons.
Users who struggle to differentiate colors may not recognize these elements as interactive.

📌 Why is this important?
According to the Web Content Accessibility Guidelines (WCAG), color should not be the only indicator of an interactive element.
If a button or link only changes color without another visual indication, it may cause issues such as:

❌ Difficulties for users with color blindness or low vision.
❌ Lack of sufficient contrast with surrounding text.
❌ Unclear identification of interactive elements.
⚠️ Issue Detected
The script scans for <button> and <a> elements that only use color for differentiation from normal text.
Example of problematic code:

❌ Incorrect Example (With Issue)
html
Copy
Edit
<a href="#" style="color: #0067A0;">Learn more</a>
<button style="color: #0067A0;">Continue</button>
✅ Correct Example (Fixed)
html
Copy
Edit
<a href="#" style="color: #0067A0; text-decoration: underline; font-weight: bold;">Learn more</a>
<button style="color: #0067A0; border: 2px solid #0067A0; background-color: #f0f0f0;">Continue</button>
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
from check_buttons_only_by_color import check_buttons_only_by_color

with open("test_buttons_only_by_color_error.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///path/to/test_buttons_only_by_color_error.html"
incidences = check_buttons_only_by_color(html_content, page_url)

for inc in incidences:
    print(inc)
📄 Example of a Detected Issue
If buttons or links lack additional visual cues, the tester will report:

json
Copy
Edit
{
    "title": "Buttons/links rely only on color",
    "type": "Color",
    "severity": "Low",
    "description": "Some buttons or links are identified only by color without additional visual cues. Users with visual impairments may not recognize them correctly.",
    "remediation": "Add visual cues such as `text-decoration: underline` for links, `border` for buttons, or bold text to differentiate them from normal content.",
    "wcag_reference": "1.4.1",
    "impact": "Users with color perception issues may not realize these elements are interactive.",
    "page_url": "file:///path/to/test_buttons_only_by_color_error.html",
    "affected_elements": [
        "<a href=\"#\" style=\"color: #0067A0;\">Learn more</a>",
        "<button style=\"color: #0067A0;\">Continue</button>"
    ]
}
✅ Benefits of the Tester
✔ Detects buttons and links identified only by color.
✔ Highlights affected elements and their code.
✔ Improves accessibility for users with visual impairments.
✔ Easy integration with global_tester.py.

💡 With this tester, we ensure all buttons and links are accessible! 🚀

