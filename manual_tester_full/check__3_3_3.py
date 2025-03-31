from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

# 1) Palabras típicas para indicar error (ES/EN)
ERROR_KEYWORDS = [
    "error", "erróneo", "erroneo", "invalid", "inválido", "incorrect",
    "incorrecto", "fallido", "falló", "fallo", "wrong"
]

# 2) Palabras o patrones que indiquen sugerencia de corrección (ES/EN)
#    Incluye verbos (“ingrese”, “introduce”, “enter”, etc.) y otras frases
#    (“debe ser”, “should be”, “use the format”, “ejemplo”, “for example” ...)
SUGGESTION_PATTERNS = [
    # Español
    "ingrese", "introduce", "por favor", "debe ser", "debes ser", "formato",
    "use", "solo dígitos", "solo letras", "ejemplo", "entre", "rango",
    "puedes", "debes", "mayor que", "menor que",

    # Inglés
    "enter", "insert", "please", "should be", "must be", "expected", 
    "format", "use the", "use a", "only digits", "only letters", "for example",
    "like", "sample", "range", "greater than", "less than"
]

def get_element_info(element):
    """Extrae metadatos del elemento para evidencia."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:120],
        "evidence": str(element)[:300]
    }

def format_incidence(inc):
    """Formatea la incidencia para exportar a Excel."""
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Ubica el mensaje de error y revisa si se ofrece alguna sugerencia de corrección."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "")
    }

def run_all___3_3_3(html_content, page_url, excel="issue_report.xlsx"):
    """
    Busca mensajes de error en el DOM (p, span, div, etc.) y determina si:
      - Tienen palabras clave de 'error'.
      - NO incluyen palabras que sugieran cómo corregir.

    Si detecta un mensaje con ERROR_KEYWORDS y no halla SUGGESTION_PATTERNS => reporta.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Candidatos: elementos que podrían mostrar mensajes de error
    candidates = soup.find_all(["p", "span", "div", "label", "li", "strong"])

    for element in candidates:
        text_lower = element.get_text(strip=True).lower()

        # 1) ¿Hay indicios de error?
        if any(err_kw in text_lower for err_kw in ERROR_KEYWORDS):
            # 2) ¿Hay al menos una palabra/patrón que indique sugerencia?
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
                        "Usuarios con discapacidad cognitiva o visual podrían "
                        "no saber cómo corregir el error."
                    ),
                    "page_url": page_url,
                    "element_info": get_element_info(element)
                })

    # Si no hay incidencias, agregar fila de justificación
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
