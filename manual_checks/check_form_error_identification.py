from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel 

def check_form_error_identification(html_content, page_url, excel="issue_report.xlsx"):
    """
    Analyzes the HTML to identify form errors that are not properly communicated in text,
    in compliance with WCAG 3.3.1 (Error Identification, Level A).
    
    Parameters:
    - html_content (str): HTML code of the page.
    - page_url (str): URL or file path of the analyzed document.

    Returns:
    - List of detected issues.
    """

    # Ensure BeautifulSoup can handle malformed HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    incidences = []

    # Find fields with `aria-invalid="true"`, ensuring case insensitivity
    error_fields = soup.find_all(lambda tag: 
        tag.name in ["input", "textarea", "select"] and 
        tag.has_attr("aria-invalid") and 
        tag["aria-invalid"].lower() == "true"
    )

    if not error_fields:
        print("⚠️ No fields with aria-invalid='true' found on the page:", page_url)
        return incidences  # Return empty if no errors detected

    for field in error_fields:
        field_name = field.get("name") or field.get("id") or "Unnamed field"
        error_text = None  # Reset error_text for each iteration
        element_info = {"tag": field.name, "id": field.get("id", "N/A"), "name": field.get("name", "N/A")}

        # 1️⃣ If the input has aria-describedby, check that message exclusively
        described_by = field.get("aria-describedby")
        if described_by:
            described_error = soup.find(id=described_by)
            if described_error and described_error.get_text(strip=True):
                # Ensure the message is not hidden
                if not described_error.has_attr("style") or "display: none" not in described_error["style"]:
                    error_text = described_error.get_text(strip=True)

        # 2️⃣ If aria-describedby is not present, look for an adjacent error message
        if not error_text:
            next_sibling = field.find_next_sibling()
            while next_sibling:
                if next_sibling.name in ["span", "div", "p", "small"] and "error" in " ".join(next_sibling.get("class", [])):
                    if not next_sibling.has_attr("style") or "display: none" not in next_sibling["style"]:
                        error_text = next_sibling.get_text(strip=True)
                        break  # Only take the first valid message found
                next_sibling = next_sibling.find_next_sibling()

        # 3️⃣ If no visible error message is found, generate an incidence
        if not error_text:
            incidences.append({
                "title": "Form field missing visible error message",
                "type": "Error Identification",
                "severity": "High",
                "description": f"The field '{field_name}' is marked as invalid but lacks a visible error message.",
                "remediation": "Ensure a visible text error message is present near the field or linked via aria-describedby.",
                "wcag_reference": "3.3.1",
                "impact": "Users may not understand what error needs correction.",
                "page_url": page_url,
                "resolution": "check_form_error_identification.md",
                "element_info": element_info
            })
            
    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
