import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

# Palabras o frases típicas que refieren forma
SHAPE_WORDS = [
    "circle", "square", "diamond", "arrow", "shape", "round", "icon"
]

# Palabras que refieren color
COLOR_WORDS = [
    "green", "blue", "red", "color", "purple", "yellow", "orange"
]

# Palabras o frases que refieren ubicación
LOCATION_WORDS = [
    "right", "left", "above", "below", "top", "bottom", "next to",
    "on the side", "in the corner", "in the center", "middle"
]

# Palabras clave para detectar *posibles* referencias textuales
TEXTUAL_REFERENCES = [
    r"label", r"etiquet", r"named", r"titled", r"texto", r"con nombre",
    r"con texto", r"llamad", r"identificad", r"caption", r"aria-"
]

def get_html_lines(html_content):
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(
        f"{i+1}: {snippet[i - start]}"
        for i in range(start, end)
    )
    return snippet_str

def get_element_info(element, html_lines=None):
    tag = element.name
    text = element.get_text(strip=True)[:150]
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"
    evidence = str(element)[:300]

    snippet_str = ""
    if line_number != "N/A" and html_lines:
        try:
            line_int = int(line_number)
            snippet_str = get_line_snippet(html_lines, line_int, context=2)
        except ValueError:
            pass

    return {
        "tag": tag,
        "text": text,
        "line_number": line_number,
        "evidence": evidence,
        "fragment_html": snippet_str
    }

def format_incidence(inc):
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")

    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Review the instruction text: \"{element_info.get('text')}\".\n\n"
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
        "Evidence [SS or Video]": element_info.get("evidence")
    }

def run_all___1_3_3(html_content, page_url, excel="issue_report.xlsx"):
    """
    Revisa el contenido HTML para detectar instrucciones que dependan
    únicamente de características sensoriales (forma, color, ubicación)
    sin incluir alguna referencia textual reconocible.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    instruction_tags = soup.find_all(["p", "span", "li", "div", "label", "strong"])
    textual_ref_regex = re.compile("|".join(TEXTUAL_REFERENCES), re.IGNORECASE)

    for element in instruction_tags:
        full_text = element.get_text(separator=" ", strip=True)
        text_lower = full_text.lower()

        uses_shape = any(word in text_lower for word in SHAPE_WORDS)
        uses_color = any(word in text_lower for word in COLOR_WORDS)
        uses_location = any(word in text_lower for word in LOCATION_WORDS)
        has_sensory_cue = (uses_shape or uses_color or uses_location)

        if not has_sensory_cue:
            continue

        mention_textual_ref = bool(textual_ref_regex.search(full_text))
        mention_in_quotes = bool(re.search(r"(['\"])(.*?)\1", full_text))

        if has_sensory_cue and not (mention_textual_ref or mention_in_quotes):
            info = get_element_info(element, html_lines=lines)
            raw_incidences.append({
                "title": "Instruction relies on sensory characteristics only",
                "type": "Instruction Text",
                "severity": "Medium",
                "expected_result": (
                    "Instructions should not rely solely on color, shape, or location "
                    "to identify a control."
                ),
                "actual_result": (
                    f"The text uses visual/spatial terms without textual ID: \"{full_text[:80]}...\""
                ),
                "remediation": (
                    "Add a textual reference (e.g., 'label', name, or 'titled') "
                    "to clarify the target control or action."
                ),
                "wcag_reference": "1.3.3",
                "impact": (
                    "Users who rely on assistive technologies may not understand "
                    "how to interact with the interface."
                ),
                "page_url": page_url,
                "element_info": info
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
            "Failed checkpoint": "1.3.3",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
