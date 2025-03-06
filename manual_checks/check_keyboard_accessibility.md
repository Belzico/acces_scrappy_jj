# 🎹 Keyboard Accessibility Tester - `check_keyboard_accessibility.py`

This script detects **mouse-only event handlers that lack keyboard equivalents**, ensuring compliance with **WCAG 2.1.1 (Keyboard Accessibility, Level A)**.

## 📌 Why is this important?
Users who rely on **keyboard navigation** or assistive technologies need to interact with all elements on a webpage without requiring a mouse.  
If elements rely **only on mouse events** (e.g., `onclick`, `mouseover`, `mouseenter`), the following issues may occur:

- ❌ **Users without a mouse cannot trigger essential functionalities.**
- ❌ **Hover-based interactions become inaccessible to keyboard users.**
- ❌ **JavaScript event listeners may exclude non-mouse users.**

---

## ⚠️ **Detected Issues**
The script scans for **elements with mouse-only interactions** and provides remediation suggestions.

### 1️⃣ **Elements with mouse events but no keyboard support**
   - **Detects elements that use `onclick`, `onmouseover`, or `onmouseenter` but lack keyboard-friendly alternatives like `onkeydown` or `onfocus`.**
   - **Incorrect example:**  
   ```html
   <div onclick="showMenu()">Open Menu</div>
Solution:
html
Copy
Edit
<div onclick="showMenu()" onkeydown="showMenu()" tabindex="0">Open Menu</div>
2️⃣ JavaScript event listeners missing keyboard equivalents
Detects addEventListener('click', ...) without a corresponding keydown event.
Incorrect example:
js
Copy
Edit
document.getElementById("menu").addEventListener("click", showMenu);
Solution:
js
Copy
Edit
document.getElementById("menu").addEventListener("click", showMenu);
document.getElementById("menu").addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") showMenu();
});
Detects addEventListener('mouseover', ...) without focus.
Incorrect example:
js
Copy
Edit
element.addEventListener("mouseover", highlightElement);
Solution:
js
Copy
Edit
element.addEventListener("mouseover", highlightElement);
element.addEventListener("focus", highlightElement);
3️⃣ Hidden elements missing aria-hidden
Detects element.style.display = 'none' without aria-hidden="true".
Incorrect example:
js
Copy
Edit
element.style.display = "none";
Solution:
js
Copy
Edit
element.style.display = "none";
element.setAttribute("aria-hidden", "true");
4️⃣ Elements with data-event="mouseover" lacking onfocus
Detects interactive elements that rely only on hover but do not support keyboard focus.
Incorrect example:
html
Copy
Edit
<div data-event="mouseover">Tooltip</div>
Solution:
html
Copy
Edit
<div data-event="mouseover" onfocus="showTooltip()">Tooltip</div>
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
from check_keyboard_accessibility import check_keyboard_accessibility

with open("test_keyboard_accessibility.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///path/to/test_keyboard_accessibility.html"
incidences = check_keyboard_accessibility(html_content, page_url)

for inc in incidences:
    print(inc)
📄 Example of a Detected Issue
If an element has onclick but lacks onkeydown, the tester will generate the following report:

json
Copy
Edit
{
    "title": "Element with mouse event lacks keyboard support",
    "type": "Keyboard Accessibility",
    "severity": "High",
    "description": "The element has onclick but lacks onkeydown.",
    "remediation": "Ensure that onkeydown is present for keyboard accessibility.",
    "wcag_reference": "2.1.1",
    "impact": "Users without a mouse cannot interact with this element.",
    "page_url": "file:///path/to/test_keyboard_accessibility.html",
    "resolution": "check_keyboard_accessibility.md",
    "element_info": {
        "tag": "div",
        "id": "menu",
        "class": "menu-button",
        "line_number": 45
    }
}
✅ Benefits of Using This Tester
✔ Detects elements that are inaccessible via keyboard.
✔ Ensures JavaScript event listeners include keyboard equivalents.
✔ Improves compliance with WCAG 2.1.1 and screen reader usability.
✔ Automatically generates an Excel report for issue tracking.

💡 With this tester, we ensure that web content is accessible to all users! 🚀