from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

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
            "2. Look for passages of text in a different language without a valid `lang` attribute.\n"
            "3. Ensure that assistive technologies can detect the change in language."
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

def run_all___3_1_2(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    known_lang_tags = {"en", "es", "fr", "de", "it", "zh", "ar", "pt", "ja", "ru", "ko"}
    all_elements = soup.find_all(True)

    for elem in all_elements:
        lang = elem.attrs.get("lang")
        if lang and lang.lower() not in known_lang_tags:
            raw_incidences.append({
                "title": "Suspicious or invalid `lang` attribute for language change",
                "type": "Language Detection",
                "severity": "Medium",
                "expected_result": "Passages of text in a different language must have a valid `lang` attribute.",
                "actual_result": f"Element has `lang='{lang}'` which may be incorrect or unrecognized.",
                "remediation": "Use valid language subtags (e.g., `lang=\"fr\"`, `lang=\"de\"`) to mark foreign phrases.",
                "wcag_reference": "3.1.2",
                "impact": "Screen readers may mispronounce the content due to incorrect language detection.",
                "page_url": page_url,
                "element_info": get_element_info(elem)
            })

        if not lang and elem.string:
            text = elem.get_text(strip=True)
            if any(word in text for word in ["voiture", "Treppenwitz", "Beaux-Arts", "habeas corpus", "Energie"]):
                raw_incidences.append({
                    "title": "Unmarked foreign language phrase",
                    "type": "Language Detection",
                    "severity": "Medium",
                    "expected_result": "Foreign phrases should be explicitly marked with a `lang` attribute.",
                    "actual_result": f"Text appears to be in another language without a lang attribute: \"{text[:60]}...\"",
                    "remediation": "Mark foreign phrases using `lang` (e.g., `<span lang=\"fr\">bonjour</span>`).",
                    "wcag_reference": "3.1.2",
                    "impact": "Assistive tech won't switch pronunciation rules appropriately.",
                    "page_url": page_url,
                    "element_info": get_element_info(elem)
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
            "Failed checkpoint": "3.1.2",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
