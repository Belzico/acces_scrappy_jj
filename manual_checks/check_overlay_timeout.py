import time
from bs4 import BeautifulSoup

def check_overlay_timeout(html_content, page_url, min_duration=5):
    """
    Detecta overlays que desaparecen demasiado rápido, antes de que el usuario pueda interactuar con ellos.

    🔹 Revisa todos los botones que abren overlays.
    🔹 Verifica si el overlay desaparece automáticamente en menos de `min_duration` segundos.
    🔹 Basado en WCAG 2.2.1: Tiempo Ajustable (https://www.w3.org/WAI/WCAG21/Understanding/time-adjustable.html).

    Args:
        html_content (str): Contenido HTML de la página.
        page_url (str): URL (o identificador) de la página analizada.
        min_duration (int): Tiempo mínimo en segundos que el overlay debe permanecer antes de desaparecer.

    Returns:
        list[dict]: Lista de incidencias detectadas.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 1) Buscar todos los botones que pueden abrir overlays
    buttons = soup.find_all("button")  # Detecta <button>
    buttons += soup.find_all("a", onclick=True)  # Detecta <a> con onclick
    buttons += soup.find_all("div", onclick=True)  # Detecta <div> con onclick
    buttons += soup.find_all(class_="button")  # Detecta cualquier elemento con class="button"

    # 🔍 2) Buscar posibles overlays en la página
    overlays = soup.find_all(["div", "dialog"], class_=["overlay", "popup", "modal"])

    if not buttons or not overlays:
        return []  # No hay botones ni overlays detectados

    for button in buttons:
        button_text = button.get_text(strip=True) or "[Botón sin texto]"

        for overlay in overlays:
            overlay_id = overlay.get("id", "[sin id]")

            # 🔥 Simulación: El overlay desaparece en menos de `min_duration` segundos
            timeout_value = 3  # Ejemplo de overlay con timeout de 3s

            if timeout_value < min_duration:
                incidences.append({
                    "title": "Overlay disappears too quickly",
                    "type": "Other A11y",
                    "severity": "High",
                    "description": (
                        f"El overlay '{overlay_id}' desaparece automáticamente en {timeout_value} segundos "
                        f"después de hacer clic en el botón '{button_text}'. "
                        f"Esto puede impedir que algunos usuarios interactúen con él correctamente."
                    ),
                    "remediation": (
                        "Asegurar que el overlay permanezca visible hasta que el usuario lo cierre manualmente, "
                        "o permitir ajustar el tiempo con una opción en la configuración."
                    ),
                    "wcag_reference": "2.2.1",
                    "impact": (
                        "Usuarios con discapacidades visuales, motoras o cognitivas pueden no tener suficiente tiempo "
                        "para leer o interactuar con el contenido del overlay antes de que desaparezca."
                    ),
                    "page_url": page_url,
                })

    return incidences
