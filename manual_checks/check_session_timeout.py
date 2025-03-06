import time
from bs4 import BeautifulSoup

def check_session_timeout(html_content, page_url):
    """
    Verifica si la página notifica adecuadamente sobre la expiración de la sesión.

    🔹 Revisa si existe una advertencia previa al cierre de sesión (modal, alert, etc.).
    🔹 Comprueba si se usa `aria-live="assertive"` para comunicar el cierre a lectores de pantalla.
    🔹 Basado en WCAG 2.2.1: Tiempo Ajustable.
    
    Args:
        html_content (str): Contenido HTML de la página.
        page_url (str): URL (o identificador) de la página analizada.

    Returns:
        list[dict]: Lista de incidencias detectadas.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 1) Buscar una advertencia de cierre de sesión
    session_warnings = soup.find_all(class_=["session-warning", "timeout-alert", "modal-warning"])

    if not session_warnings:
        incidences.append({
            "title": "No session timeout warning",
            "type": "Screen Reader",
            "severity": "High",
            "description": (
                "No se detectó un mensaje de advertencia antes de que la sesión expire. "
                "Los usuarios de lectores de pantalla podrían ser desconectados sin previo aviso."
            ),
            "remediation": (
                "Implementar un modal de advertencia antes del cierre de sesión con `aria-live='assertive'` "
                "para que los usuarios sean notificados."
            ),
            "wcag_reference": "2.2.1",
            "impact": "Los usuarios pueden quedar bloqueados sin saber que han sido desconectados.",
            "page_url": page_url,
        })

    # 🔍 2) Verificar si la advertencia usa `aria-live="assertive"`
    for warning in session_warnings:
        aria_live = warning.get("aria-live", "").lower()
        if aria_live != "assertive":
            incidences.append({
                "title": "Session timeout warning is not screen reader friendly",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    "Se detectó una advertencia de cierre de sesión, pero no utiliza `aria-live='assertive'`, "
                    "lo que impide que sea anunciada inmediatamente a usuarios de lectores de pantalla."
                ),
                "remediation": (
                    "Añadir `aria-live='assertive'` al modal o alerta de advertencia."
                ),
                "wcag_reference": "2.2.1",
                "impact": "Usuarios con discapacidades no serán notificados a tiempo sobre la expiración de la sesión.",
                "page_url": page_url,
            })

    return incidences
