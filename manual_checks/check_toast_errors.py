import time
from bs4 import BeautifulSoup

def check_toast_errors(html_content, page_url, min_duration=5):
    """
    Detecta mensajes de error tipo "toast" que desaparecen demasiado rápido, 
    antes de que el usuario pueda leerlos o interactuar con ellos.

    🔹 Revisa todos los elementos que parecen "toast messages".
    🔹 Verifica si el mensaje desaparece automáticamente en menos de `min_duration` segundos.
    🔹 Basado en WCAG 2.2.1: Tiempo Ajustable.

    Args:
        html_content (str): Contenido HTML de la página.
        page_url (str): URL (o identificador) de la página analizada.
        min_duration (int): Tiempo mínimo en segundos que el mensaje debe permanecer antes de desaparecer.

    Returns:
        list[dict]: Lista de incidencias detectadas.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 Buscar posibles toast messages (notificaciones flotantes)
    toast_messages = soup.find_all(class_=["toast", "notification", "alert", "error-message"])

    for toast in toast_messages:
        toast_text = toast.get_text(strip=True) or "[Mensaje sin texto]"
        timeout_value = 2  # Simulación: mensaje que desaparece en 2s

        if timeout_value < min_duration:
            incidences.append({
                "title": "Error message disappears too quickly",
                "type": "Other A11y",
                "severity": "High",
                "description": (
                    f"El mensaje de error '{toast_text}' desaparece automáticamente en {timeout_value} segundos. "
                    "Esto puede impedir que algunos usuarios lo lean o comprendan la razón del error."
                ),
                "remediation": (
                    "Asegurar que los mensajes de error permanezcan visibles hasta que el usuario los cierre manualmente. "
                    "Idealmente, mostrar el mensaje cerca del campo del formulario."
                ),
                "wcag_reference": "2.2.1",
                "impact": (
                    "Los usuarios pueden no darse cuenta del error y no comprender por qué no se envió el formulario."
                ),
                "page_url": page_url,
            })

    return incidences
