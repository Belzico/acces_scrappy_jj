from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def get_element_info(element):
    """Retrieves useful information about an HTML element to facilitate issue identification."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # First 50 characters of the text
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"  # Gets line number if available
    }

def check_accordion_aria_expanded(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks whether accordion buttons have the `aria-expanded` attribute properly configured.
    
    - Identifies all accordions (buttons with `aria-expanded` or `role="button"`).
    - If any button lacks `aria-expanded="true"` or `aria-expanded="false"`, an issue is reported.
    """

    # 1️⃣ Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2️⃣ Find all potential accordion buttons
    accordion_buttons = soup.find_all("button", class_="accordion-toggle")  # Standard buttons
    accordion_buttons += soup.find_all(attrs={"role": "button", "class": "accordion-toggle"})  # Elements with role="button"
    accordion_buttons += soup.find_all("a", class_="accordion-toggle")  # Optionally, links

    if not accordion_buttons:
        return []  # No accordions found, no issue generated

    incorrect_buttons = [
        btn for btn in accordion_buttons if btn.get("aria-expanded") not in ["true", "false"]
    ]

    incidences = []
    if incorrect_buttons:
        for btn in incorrect_buttons:
            incidences.append({
                "title": "Accordion items do not announce their state",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": "One or more accordion buttons are missing the `aria-expanded` attribute. "
                               "This prevents screen reader users from knowing whether the accordion is expanded or collapsed.",
                "remediation": "Add `aria-expanded=\"true\"` or `aria-expanded=\"false\"` to the accordion button. "
                               "Example: `<button aria-expanded=\"false\">Section 1</button>`.",
                "wcag_reference": "4.1.2",
                "impact": "Screen reader users may not be aware of expandable content on the page.",
                "page_url": page_url,
                "resolution": "check_accordion_aria_expanded.md",
                "element_info": get_element_info(btn)
            })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
