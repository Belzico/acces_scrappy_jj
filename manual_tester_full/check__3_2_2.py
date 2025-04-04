import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

CHANGE_CONTEXT_PATTERNS = [
    r"window\.open",
    r"location\.href",
    r"top\.location",
    r"self\.location",
    r"document\.location",
    r"\.submit\s*\("
]

def get_html_lines(html_content):
    """Convierte el contenido HTML a una lista de líneas."""
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    Extrae un fragmento de contexto alrededor de line_number (2 líneas antes/después).
    Añade numeración para facilitar la depuración.
    """
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Reúne metadatos del elemento (tag + snippet) e incluye un fragmento
    de HTML alrededor de la línea line_number si está disponible.
    """
    tag = element.name
    attrs = dict(element.attrs)
    snippet_html = str(element)[:300]
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

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
    """Arma la incidencia para el Excel, mostrando también el snippet de HTML contextual."""
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")

    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Locate the UI control (e.g. <select> or <input>) with an `onchange` or similar event.\n"
            "3. Verify if changing the value triggers a context change with no prior warning.\n\n"
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

def run_all___3_2_2(html_content, page_url, excel="issue_report.xlsx"):
    """
    1. Parsea el HTML.
    2. Busca <select> y <input type=checkbox/radio> con event handlers como 'onchange', 'onclick', etc.
    3. Revisa si el handler coincide con un cambio de contexto (abrir ventana, redirigir, etc.).
    4. Reporta si no hay aviso previo.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    # 1) Buscar selects
    selects = soup.find_all("select")
    for sel in selects:
        possible_events = []
        if sel.has_attr("onchange"):
            possible_events.append(sel["onchange"])
        if sel.has_attr("oninput"):
            possible_events.append(sel["oninput"])

        for script_value in possible_events:
            sv_lower = script_value.lower()
            if any(re.search(pattern, sv_lower) for pattern in CHANGE_CONTEXT_PATTERNS):
                raw_incidences.append({
                    "title": "Select changes context on value change without prior warning",
                    "type": "On Input Behavior",
                    "severity": "High",
                    "expected_result": (
                        "Changing a select's value should not cause context shift unless "
                        "the user is forewarned or the user explicitly triggers it."
                    ),
                    "actual_result": f"onchange/oninput has code that changes context: {script_value}",
                    "remediation": (
                        "Provide a separate submit button or an explicit warning that selecting an option "
                        "will cause a new page or window. Alternatively, wait for user confirmation."
                    ),
                    "wcag_reference": "3.2.2",
                    "impact": (
                        "Users might be disoriented if the page or window changes as soon "
                        "as they pick an item from the dropdown."
                    ),
                    "page_url": page_url,
                    "element_info": get_element_info(sel, lines)
                })

    # 2) Buscar inputs type=radio/checkbox
    inputs = soup.find_all("input", {"type": ["radio", "checkbox"]})
    for inp in inputs:
        possible_events = []
        if inp.has_attr("onchange"):
            possible_events.append(inp["onchange"])
        if inp.has_attr("oninput"):
            possible_events.append(inp["oninput"])
        if inp.has_attr("onclick"):
            possible_events.append(inp["onclick"])

        for script_value in possible_events:
            sv_lower = script_value.lower()
            if any(re.search(pattern, sv_lower) for pattern in CHANGE_CONTEXT_PATTERNS):
                raw_incidences.append({
                    "title": "Radio/Checkbox changes context on input without warning",
                    "type": "On Input Behavior",
                    "severity": "High",
                    "expected_result": (
                        "Selecting a radio/checkbox must not shift context unexpectedly. "
                        "User should be informed or confirm the action."
                    ),
                    "actual_result": f"Script triggers context change: {script_value}",
                    "remediation": (
                        "Use a separate button or confirm dialog, or clearly warn the user that checking "
                        "this box/radio triggers new context."
                    ),
                    "wcag_reference": "3.2.2",
                    "impact": (
                        "Users with motor or cognitive disabilities may not expect the page to reload "
                        "or open a new window upon simply checking a box."
                    ),
                    "page_url": page_url,
                    "element_info": get_element_info(inp, lines)
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
            "Failed checkpoint": "3.2.2",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
