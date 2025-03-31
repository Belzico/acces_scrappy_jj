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

def get_element_info(element):
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:150],  # hasta 150 chars
        "evidence": str(element)[:300]               # recorte
    }

def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Review the instruction text: \"{inc.get('element_info', {}).get('text')}\"."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence")
    }

def run_all___1_3_3(html_content, page_url, excel="issue_report.xlsx"):
    """
    Revisa el contenido HTML para detectar instrucciones que dependan
    únicamente de características sensoriales (forma, color, ubicación)
    sin incluir alguna referencia textual reconocible.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Buscamos en los elementos que normalmente contienen instrucciones.
    # Podrías ampliarlo a otros: h2, h3, strong, etc. si lo ves necesario.
    instruction_tags = soup.find_all(["p", "span", "li", "div", "label", "strong"])

    # Compilemos regex para textual references (mejora de performance).
    textual_ref_regex = re.compile("|".join(TEXTUAL_REFERENCES), re.IGNORECASE)

    for element in instruction_tags:
        full_text = element.get_text(separator=" ", strip=True)
        text_lower = full_text.lower()

        # 1) Verificar si se utilizan palabras sensoriales
        uses_shape = any(word in text_lower for word in SHAPE_WORDS)
        uses_color = any(word in text_lower for word in COLOR_WORDS)
        uses_location = any(word in text_lower for word in LOCATION_WORDS)
        has_sensory_cue = (uses_shape or uses_color or uses_location)

        if not has_sensory_cue:
            # Si ni siquiera hay palabras clave sensoriales, no nos interesa.
            continue

        # 2) Verificar si hay alguna referencia textual en la misma frase
        #    p. ej., "botón etiquetado como 'Continuar'", "named 'Save'", etc.
        #    o la presencia de comillas ("..." o '...') que sugieran un identificador textual.
        mention_textual_ref = bool(textual_ref_regex.search(full_text))
        mention_in_quotes = bool(re.search(r"(['\"])(.*?)\1", full_text))

        # Heurística: si hay keywords sensoriales,
        # pero no hay referencia textual NI algo en comillas => posible error
        # (Si hay comillas, presumimos que es un identificador textual).
        if has_sensory_cue and not (mention_textual_ref or mention_in_quotes):
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
                "element_info": get_element_info(element)
            })

    # Si no se encontraron incidencias, agregamos una fila de justificación
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

    # Exportamos a Excel y retornamos
    transform_json_to_excel(formatted, excel)
    return formatted
