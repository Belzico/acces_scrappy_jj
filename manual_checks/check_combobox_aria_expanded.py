from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def get_element_info(element):
    """Retrieves useful information about an HTML element to facilitate issue identification."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # First 50 characters of the text
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"
    }

def check_combobox_aria_expanded(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if search comboboxes have `aria-expanded` correctly configured.

    - Looks for inputs with `role="combobox"`, divs with `role="combobox"`, and selects.
    - Verifies if they have `aria-expanded="true"` or `aria-expanded="false"`.
    - If `aria-expanded` does not change correctly, an issue is generated.
    """

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all potential comboboxes
    comboboxes = []
    
    # a) Inputs with role="combobox"
    comboboxes += soup.find_all("input", attrs={"role": "combobox"})
    
    # b) Divs with role="combobox"
    comboboxes += soup.find_all("div", attrs={"role": "combobox"})
    
    # c) Selects with aria-expanded (not common, but some use it)
    comboboxes += soup.find_all("select", attrs={"aria-expanded": True})

    if not comboboxes:
        return []  # No comboboxes found

    incorrect_comboboxes = [
        cb for cb in comboboxes if cb.get("aria-expanded") not in ["true", "false"]
    ]

    incidences = []
    for cb in incorrect_comboboxes:
        incidences.append({
            "title": "Search combobox missing aria-expanded",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": "One or more search comboboxes do not properly update the `aria-expanded` attribute. "
                           "When the search menu expands, `aria-expanded` should change to `true`, "
                           "and when collapsed, it should change to `false`.",
            "remediation": "Ensure that the search combobox updates its `aria-expanded` attribute properly. "
                           "Example: `<input role=\"combobox\" aria-expanded=\"true\">` when expanded.",
            "wcag_reference": "4.1.2",
            "impact": "Screen reader users may be confused if `aria-expanded` does not correctly update on search elements.",
            "page_url": page_url,
            "resolution": "check_combobox_aria_expanded.md",
            "element_info": get_element_info(cb)
        })

    # Convert incidences to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
