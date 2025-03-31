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

def get_element_info(element):
    """Reúne metadatos para el reporte."""
    return {
        "tag": element.name,
        "snippet": str(element)[:300]
    }

def format_incidence(inc):
    """Arma el dict final para exportar a Excel."""
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            "2. Locate the form or button with potential legal/financial/data-critical action.\n"
            "3. Check if there's no review/confirmation/cancellation step."
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

def run_all___3_3_4(html_content, page_url, excel="issue_report.xlsx"):
    """
    Heurística:
      - Busca formularios o botones que contengan palabras clave críticas (compras, borrados, transacciones)
      - Si no encuentra palabras o elementos que sugieran confirmación, revisión o deshacer => Incidencia.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # Buscamos <form> y <button> (o <input type=submit/button>) con keywords
    forms = soup.find_all("form")
    buttons = soup.find_all(["button", "input"], {
        "type": ["submit", "button"]
    })

    # Revisaremos ambos sets (forms y botones) en un array unificado con metadata
    critical_elements = []

    # 1) Revisar forms
    for f in forms:
        text = f.get_text(strip=True).lower()
        if any(crit in text for crit in CRITICAL_KEYWORDS):
            critical_elements.append(f)

    # 2) Revisar botones
    for b in buttons:
        # Podríamos unir el texto del botón + su parent
        text_button = b.get_text(strip=True).lower() or ""
        # Considerar "value" si es input type=submit
        val = b.get("value", "").lower()
        parent_text = b.find_parent().get_text(strip=True).lower() if b.find_parent() else ""
        text_combined = text_button + " " + val + " " + parent_text

        if any(crit in text_combined for crit in CRITICAL_KEYWORDS):
            critical_elements.append(b)

    # Para cada elemento crítico => chequeamos si hay "review / confirm / cancel..."
    for elem in critical_elements:
        # Ver si en su texto (o el de su padre) hay SAFETY_KEYWORDS
        txt = elem.get_text(strip=True).lower() if hasattr(elem, "get_text") else ""
        parent_txt = elem.find_parent().get_text(strip=True).lower() if elem.find_parent() else ""
        combined_txt = txt + " " + parent_txt

        # Buscar en la vecindad
        # Heurística: si no está ANY de SAFETY_KEYWORDS => error
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
                    "Found keywords suggesting an important transaction or data deletion, but "
                    "no sign of confirmation or review step."
                ),
                "remediation": (
                    "Add a confirmation dialog, review page, or undo option for user to verify/correct."
                ),
                "wcag_reference": "3.3.4",
                "impact": (
                    "Users could accidentally finalize significant transactions or lose data "
                    "without a chance to reverse or correct."
                ),
                "page_url": page_url,
                "element_info": get_element_info(elem)
            })

    # Si no se encontró incidencia
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
