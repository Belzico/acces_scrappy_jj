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

def check_aria_label_in_div(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if there are `<div>` elements with `aria-label` but without a valid `role`.

    - Finds all `<div>` elements with the `aria-label` attribute.
    - Checks if they have a valid `role` attribute.
    - If the `role` is missing, an issue is generated.
    """

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <div> elements with aria-label
    divs_with_aria_label = soup.find_all("div", attrs={"aria-label": True})

    # Filter those without a defined role
    invalid_divs = [div for div in divs_with_aria_label if not div.has_attr("role")]

    incidences = []
    for div in invalid_divs:
        incidences.append({
            "title": "ARIA label used in <div> without a role",
            "type": "HTML Validator",
            "severity": "Low",
            "description": "The `aria-label` attribute should only be used on elements that support it. "
                           "Currently, it is applied to a `<div>` without a defined `role`, which is not valid.",
            "remediation": "Ensure that `<div>` elements with `aria-label` have an appropriate `role`, such as `role=\"button\"`, `role=\"option\"`, etc. "
                           "If `aria-label` is not necessary, consider using a `<span>` or `<button>` instead.",
            "wcag_reference": "4.1.2",
            "impact": "No immediate impact, but it may cause issues in validators and assistive technologies.",
            "page_url": page_url,
            "resolution": "check_aria_label_in_div.md",
            "element_info": get_element_info(div)
        })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
