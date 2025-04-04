import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

ERROR_KEYWORDS = [
    "error", "erróneo", "erroneo", "invalid", "inválido", "incorrect",
    "incorrecto", "fallido", "falló", "fallo", "wrong"
]

SUGGESTION_PATTERNS = [
    "ingrese", "introduce", "por favor", "debe ser", "debes ser", "formato",
    "use", "solo dígitos", "solo letras", "ejemplo", "entre", "rango",
    "puedes", "debes", "mayor que", "menor que",
    "enter", "insert", "please", "should be", "must be", "expected", 
    "format", "use the", "use a", "only digits", "only letters", "for example",
    "like", "sample", "range", "greater than", "less than"
]

def get_html_lines(html_content):
    """Convierte el contenido HTML en lista de líneas para extraer fragmentos contextuales."""
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    Extrae un snippet con `context` líneas antes y después de line_number (base 1).
    Devuelve un string con numeración para cada línea.
    """
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Extrae metadatos del elemento para evidencia, incluyendo un snippet
    de HTML alrededor de la línea donde se encuentra (si está disponible).
    """
    tag = element.name
    text = element.get_text(strip=True)[:120]
    evidence = str(element)[:300]
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"
    fragment_html = ""

    if line_number != "N/A" and html_lines:
        try:
            fragment_html = get_line_snippet(html_lines, int(line_number), context=2)
        except Exception:
            pass

    return {
        "tag": tag,
        "text": text,
        "evidence": evidence,
        "line_number": line_number,
        "fragment_html": fragment_html
    }

def format_incidence(inc):
    """Formatea la incidencia para exportar a Excel, mostrando también el snippet HTML contextual."""
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")

    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Ubica el mensaje de error y revisa si se ofrece alguna sugerencia de corrección.\n\n"
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
        "Evidence [SS or Video]": element_info.get("evidence", "")
    }

def run_all___3_3_3(html_content, page_url, excel="issue_report.xlsx"):
    """
    Busca mensajes de error en el DOM y determina si incluyen sugerencias de corrección.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    candidates = soup.find_all(["p", "span", "div", "label", "li", "strong"])
    for element in candidates:
        text_lower = element.get_text(strip=True).lower()
        # 1) ¿Hay indicios de error?
        if any(err_kw in text_lower for err_kw in ERROR_KEYWORDS):
            # 2) ¿Existe sugerencia/pista de corrección?
            if not any(sugg_kw in text_lower for sugg_kw in SUGGESTION_PATTERNS):
                raw_incidences.append({
                    "title": "Error message without corrective suggestion",
                    "type": "Form Error",
                    "severity": "High",
                    "expected_result": (
                        "Los mensajes de error deben incluir sugerencias claras para corregir."
                    ),
                    "actual_result": f"Mensaje: \"{element.get_text(strip=True)}\" carece de pista de corrección.",
                    "remediation": (
                        "Incluye frases indicando cómo corregir el error, e.g. "
                        "\"Por favor ingrese un número entre 1 y 10\" o \"Enter a valid format: user@example.com\"."
                    ),
                    "wcag_reference": "3.3.3",
                    "impact": (
                        "Usuarios con discapacidad cognitiva o visual podrían no saber cómo corregir el error."
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
            "Failed checkpoint": "3.3.3",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
