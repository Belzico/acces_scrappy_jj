import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_html_lines(html_content):
    """Divide el HTML en una lista de líneas, para extraer fragmentos de contexto."""
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """Retorna el fragmento de HTML alrededor de line_number (2 líneas antes/después)."""
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(f"{i+1}: {snippet[i - start]}" for i in range(start, end))
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Extrae metadatos del elemento y un snippet del HTML circundante.
    """
    tag = element.name
    attrs = dict(element.attrs)
    snippet_html = str(element)[:300]  # Truncado a 300 chars
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"
    
    fragment = ""
    if line_number != "N/A" and html_lines:
        try:
            fragment = get_line_snippet(html_lines, int(line_number), context=2)
        except Exception:
            pass

    return {
        "tag": tag,
        "attrs": attrs,
        "snippet": snippet_html,
        "line_number": line_number,
        "fragment_html": fragment
    }

def format_incidence(inc):
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Identify the interactive element and measure its size and spacing.\n"
            "3. Check if it meets the 24x24 CSS pixels minimum or the spacing exception.\n\n"
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

def run_all___2_5_8(html_content, page_url, excel="issue_report.xlsx"):
    """
    Verifica que los elementos interactivos cumplan la regla de 24x24 CSS px, 
    o provean la excepción de espaciamiento suficiente.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    INTERACTIVE_TAGS = ["button", "a", "input", "label", "textarea", "select"]
    for element in soup.find_all(INTERACTIVE_TAGS):
        style = element.get("style", "")
        width, height = None, None
        if "px" in style:
            for part in style.split(";"):
                part_strip = part.strip().lower()
                if "width" in part_strip:
                    try:
                        width_val = part_strip.split(":")[1].replace("px", "").strip()
                        width = int(width_val)
                    except:
                        pass
                if "height" in part_strip:
                    try:
                        height_val = part_strip.split(":")[1].replace("px", "").strip()
                        height = int(height_val)
                    except:
                        pass

        if width is not None and height is not None and (width < 24 or height < 24):
            raw_incidences.append({
                "title": "Target smaller than 24x24 CSS pixels",
                "type": "Target Size (Minimum)",
                "severity": "Medium",
                "expected_result": (
                    "Interactive elements should be at least 24x24 CSS pixels, "
                    "or have sufficient spacing around them to avoid accidental activation."
                ),
                "actual_result": f"Element <{element.name}> has dimensions width: {width}px, height: {height}px.",
                "remediation": (
                    "Increase the size of the target to 24x24 pixels or provide adequate spacing "
                    "(using 24px diameter spacing rule) from adjacent targets."
                ),
                "wcag_reference": "2.5.8",
                "impact": (
                    "Users with motor disabilities or touch input may struggle to activate small or tightly packed targets."
                ),
                "page_url": page_url,
                "element_info": get_element_info(element, html_lines=lines)
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
            "Failed checkpoint": "2.5.8",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
