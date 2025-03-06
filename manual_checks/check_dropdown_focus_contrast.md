📋 Dropdown Focus Contrast Checker
📝 Description
This tester checks whether dropdown (<select>) options have sufficient color contrast when selected or focused. It ensures compliance with WCAG 2.1 – Success Criterion 1.4.11 (Non-text Contrast).

🔍 What It Checks
Finds <select> elements and their <option> elements.
Detects applied CSS styles (color and background).
Calculates contrast ratio between text and background.
Reports violations if contrast ratio is below 3:1.
🚨 Why It Matters
Users with low vision may struggle to distinguish selected or hovered options in dropdown menus if there is insufficient color contrast.

✅ Example of a Good Dropdown
html
Copy
Edit
<select>
  <option selected style="color: #000; background-color: #f1f1f1;">
    Selected Option
  </option>
</select>
✅ Passes contrast ratio check (3:1 or higher).

❌ Example of a Bad Dropdown
html
Copy
Edit
<select>
  <option selected style="color: #ccc; background-color: #fff;">
    Selected Option
  </option>
</select>
❌ Fails contrast ratio check (below 3:1).

📊 Test Details
Field	Details
Title	Dropdown selected/hovered option fails color contrast requirements
Type	Color Contrast
Severity	High
WCAG Reference	1.4.11: Non-text Contrast
Impact	Users with low vision may not distinguish selected or focused dropdown options.
Resolution	check_dropdown_focus_contrast.md
🛠 Recommended Fix
Ensure the contrast ratio is at least 3:1 between the text and background.
Use darker backgrounds or lighter text.
Example:
css
Copy
Edit
option[selected] {
  color: #000; 
  background-color: #ddd;
}
📌 This fix improves accessibility for users with visual impairments. 🚀