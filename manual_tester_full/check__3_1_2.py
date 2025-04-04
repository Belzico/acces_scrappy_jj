import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_html_lines(html_content):
    """
    Divide el HTML en lista de líneas, útil para extraer
    fragmentos de contexto alrededor de line_number.
    """
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    Obtiene un fragmento de 'context' líneas antes y después de line_number.
    """
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    # Agregamos numeración de líneas
    snippet_str = "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Retorna datos básicos del elemento y un snippet de HTML
    alrededor de su line_number (si existe).
    """
    tag = element.name
    attrs = dict(element.attrs)
    snippet_html = str(element)[:300]  # Muestra hasta 300 chars del elemento
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    fragment_html = ""
    if line_number != "N/A" and html_lines:
        try:
            fragment_html = get_line_snippet(html_lines, int(line_number), context=2)
        except Exception:
            pass

    return {
        "tag": tag,
        "attrs": attrs,
        "snippet": snippet_html,
        "line_number": line_number,
        "fragment_html": fragment_html
    }

def format_incidence(inc):
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")

    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Look for passages of text in a different language without a valid `lang` attribute.\n"
            "3. Ensure that assistive technologies can detect the change in language.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n"
            f"{snippet}"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": element_info.get("snippet", "")
    }

def run_all___3_1_2(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    known_lang_tags = {"en", "es", "fr", "de", "it", "zh", "ar", "pt", "ja", "ru", "ko"}
    all_elements = soup.find_all(True)

    for elem in all_elements:
        lang = elem.attrs.get("lang")
        # 1) lang con valor no reconocido
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
                "element_info": get_element_info(elem, html_lines=lines)
            })

        # 2) Texto que podría indicar otro idioma sin `lang`
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
                    "element_info": get_element_info(elem, html_lines=lines)
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
