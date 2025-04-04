import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_html_lines(html_content):
    """Convierte el contenido HTML en lista de líneas para extraer fragmentos de contexto."""
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    Extrae un snippet de 'context' líneas antes y después de line_number (base 1),
    y devuelve el texto con line numbering para depuración.
    """
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Extrae metadatos del elemento y un snippet de HTML alrededor
    de la línea en la que se encuentra.
    """
    tag = element.name
    attrs = dict(element.attrs)
    snippet_html = str(element)[:300]
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    fragment_html = ""
    if line_number != "N/A" and html_lines:
        try:
            fragment_html = get_line_snippet(html_lines, int(line_number), context=2)
        except ValueError:
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
            "2. Check the form field identified below. There's no label or instruction.\n\n"
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

def run_all___3_3_2(html_content, page_url, excel="issue_report.xlsx"):
    """
    Heurística:
    - Busca <input> (type != hidden/button/submit/reset/file), <select>, <textarea>
    - Ve si tienen label for=ID o aria-label/aria-labelledby o placeholder
    - Si no => error: Falta label/instrucción
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    valid_input_types = [
        "text", "password", "email", "number", "search", "tel", "url", "date",
        "datetime-local", "month", "time", "week", "radio", "checkbox"
    ]

    form_fields = []
    inputs = soup.find_all("input")
    for inp in inputs:
        t = (inp.get("type") or "text").lower()
        if t in valid_input_types:
            form_fields.append(inp)

    selects = soup.find_all("select")
    form_fields.extend(selects)

    textareas = soup.find_all("textarea")
    form_fields.extend(textareas)

    for field in form_fields:
        field_id = field.get("id", "")
        has_label = False

        # Revisar <label for="field_id">
        if field_id:
            label = soup.find("label", {"for": field_id})
            if label and label.get_text(strip=True):
                has_label = True

        aria_label = field.get("aria-label", "")
        aria_labelledby = field.get("aria-labelledby", "")
        if aria_label.strip():
            has_label = True
        if aria_labelledby.strip():
            has_label = True

        placeholder = field.get("placeholder", "")
        if placeholder.strip():
            has_label = True

        if not has_label:
            raw_incidences.append({
                "title": "Form field without visible label or instructions",
                "type": "Labels or Instructions",
                "severity": "Medium",
                "expected_result": (
                    "Each input/select/textarea requiring user input must have a label or instructions."
                ),
                "actual_result": (
                    "No <label for>, no aria-label/aria-labelledby, no placeholder found."
                ),
                "remediation": (
                    "Add a <label> or instructions so the user knows what info to enter. "
                    "Alternatively, set aria-label or a placeholder as minimal fallback."
                ),
                "wcag_reference": "3.3.2",
                "impact": (
                    "Users, especially with cognitive disabilities, won't know what data is expected here."
                ),
                "page_url": page_url,
                "element_info": get_element_info(field, html_lines=lines)
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
            "Failed checkpoint": "3.3.2",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
