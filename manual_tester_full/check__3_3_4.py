import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

# Palabras típicas que sugieren acción con consecuencias legales/financieras o
# que modifican/borran datos del usuario.
CRITICAL_KEYWORDS = [
    # Finanzas/Compras
    "buy", "purchase", "checkout", "pay now", "pay", "order", "confirm order",
    "finalize", "transaction", "billing", "shipping", "credit card", "loan", "stock", "bank",
    # Legales
    "legal", "contract", "terms and conditions", "tax", "invoice",
    # Datos de usuario
    "delete account", "remove account", "delete data", "remove data", "delete record", "remove record",
    "update profile", "modify profile", "clear data", "permanently delete",
    # Exámenes / pruebas
    "test submission", "submit test", "exam submission"
]

# Palabras que indicarían confirmación, revisión o posibilidad de revertir
SAFETY_KEYWORDS = [
    "review", "confirm", "are you sure", "undo", "cancel", "edit before submitting",
    "change your mind", "recover", "restore", "back button", "preview", "time window to cancel",
    "amend", "cancel order", "double-check"
]

def get_html_lines(html_content):
    """
    Convierte todo el contenido HTML en una lista de líneas
    para luego extraer fragmentos de contexto.
    """
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    Extrae un snippet con 2 líneas antes y 2 después de line_number (base 1).
    Añade numeración para depurar.
    """
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Reúne metadatos para el reporte, incluyendo un snippet
    de 2 líneas antes y 2 después del line_number del elemento.
    """
    tag = element.name
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
        "snippet": snippet_html,
        "line_number": line_number,
        "fragment_html": fragment_html
    }

def format_incidence(inc):
    """
    Construye el dict final para exportar a Excel,
    mostrando también el snippet HTML contextual.
    """
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Locate the form or button with potential legal/financial/data-critical action.\n"
            "3. Check if there's no review/confirmation/cancellation step.\n\n"
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

def run_all___3_3_4(html_content, page_url, excel="issue_report.xlsx"):
    """
    Heurística:
      - Busca formularios o botones que contengan palabras clave críticas (compras, borrados, transacciones)
      - Si no encuentra palabras o elementos que sugieran confirmación, revisión o deshacer => Incidencia.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    # Buscamos <form> y <button> (o <input type=submit/button>) con keywords
    forms = soup.find_all("form")
    buttons = soup.find_all(["button", "input"], {"type": ["submit", "button"]})

    critical_elements = []

    # 1) Revisar forms
    for f in forms:
        text = f.get_text(strip=True).lower()
        if any(crit in text for crit in CRITICAL_KEYWORDS):
            critical_elements.append(f)

    # 2) Revisar botones
    for b in buttons:
        text_button = b.get_text(strip=True).lower() or ""
        val = b.get("value", "").lower()
        parent_text = b.find_parent().get_text(strip=True).lower() if b.find_parent() else ""
        text_combined = f"{text_button} {val} {parent_text}"

        if any(crit in text_combined for crit in CRITICAL_KEYWORDS):
            critical_elements.append(b)

    # Revisar si hay confirmación
    for elem in critical_elements:
        txt = elem.get_text(strip=True).lower() if hasattr(elem, "get_text") else ""
        parent_txt = elem.find_parent().get_text(strip=True).lower() if elem.find_parent() else ""
        combined_txt = f"{txt} {parent_txt}"

        if not any(safe_kw in combined_txt for safe_kw in SAFETY_KEYWORDS):
            raw_incidences.append({
                "title": "Potential high-stakes action without confirmation/review",
                "type": "Error Prevention",
                "severity": "High",
                "expected_result": (
                    "Pages with serious legal/financial/data changes must allow reversing, "
                    "reviewing or confirming the action."
                ),
                "actual_result": (
                    "Found keywords suggesting an important transaction or data deletion, "
                    "but no sign of confirmation or review step."
                ),
                "remediation": (
                    "Add a confirmation dialog, review page, or undo option for users to verify or correct the action."
                ),
                "wcag_reference": "3.3.4",
                "impact": (
                    "Users could accidentally finalize significant transactions or lose data "
                    "without a chance to reverse or correct."
                ),
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
            "Failed checkpoint": "3.3.4",
            "User Impact": "N/A",
            "Evidence [SS or Video]": "N/A"
        })

    transform_json_to_excel(formatted, excel)
    return formatted
