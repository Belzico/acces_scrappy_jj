from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  # Asegúrate de tener este módulo

def get_element_info(element):
    return {
        "tag": element.name,
        "attrs": dict(element.attrs),
        "snippet": str(element)[:300]
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Verify that the <html> element contains a valid 'lang' attribute "
            "indicating the primary language of the page (e.g., <html lang=\"en\">)."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("snippet", "")
    }

def run_all___3_1_1(html_content, page_url, excel="issue_report.xlsx"):
    """
    WCAG 3.1.1 - Language of Page:
    Verifica que el atributo 'lang' esté presente y correctamente definido en <html>.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []
    html_tag = soup.find("html")

    if html_tag:
        lang_value = html_tag.get("lang", None)
        if not lang_value or not isinstance(lang_value, str) or len(lang_value.strip()) < 2:
            raw_incidences.append({
                "title": "Missing or invalid 'lang' attribute on <html> element",
                "type": "Language Detection",
                "severity": "High",
                "expected_result": "The <html> element must have a valid 'lang' attribute indicating the primary language of the page.",
                "actual_result": "No 'lang' attribute found or invalid value set in the <html> tag.",
                "remediation": "Add or correct the 'lang' attribute in <html> (e.g., <html lang=\"en\"> or <html lang=\"es\">).",
                "wcag_reference": "3.1.1",
                "impact": "Assistive technologies may not interpret content correctly, impacting comprehension for screen reader users.",
                "page_url": page_url,
                "element_info": get_element_info(html_tag)
            })
    else:
        raw_incidences.append({
            "title": "Missing <html> element",
            "type": "Language Detection",
            "severity": "High",
            "expected_result": "The document should have a <html> root element with a 'lang' attribute.",
            "actual_result": "No <html> element found in the document.",
            "remediation": "Ensure the page starts with a valid <html> element and includes a 'lang' attribute.",
            "wcag_reference": "3.1.1",
            "impact": "The language of the page cannot be determined, which may confuse assistive technologies.",
            "page_url": page_url,
            "element_info": {}
        })

    formatted = [format_incidence(i) for i in raw_incidences]

    if not formatted:
        formatted.append({
            "Title": "Justificación de los CPs asignados que no generen issues",
            "Steps": "N/A",
            "Bug Type": "N/A",
            "Priority": "N/A",
            "Expected Result": "N/A",
            "Actual Result": "N/A",
            "Suggested resolution(s)": "N/A",
            "Failed checkpoint": "3.1.1",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
