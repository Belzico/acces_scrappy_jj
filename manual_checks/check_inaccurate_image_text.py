# manual_checks/check_informative_images.py

import os
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image

def check_informative_images(html_content, page_url):
    """
    Verifica si las imágenes (consideradas informativas) tienen un alt adecuado y,
    opcionalmente, compara el texto real (vía OCR) con el alt.
    
    - Busca las imágenes dentro de la carpeta 'downloaded_images'.
    - Si el alt es nulo/vacío -> Error.
    - Si el alt es genérico (ej. "image") -> Incidencia.
    - Aplica OCR si existe la imagen en 'downloaded_images' y compara con el alt.
    
    Basado en la doc oficial de W3C para “Informative Images”:
    https://www.w3.org/WAI/tutorials/images/informative/
    
    Requisitos:
      - Tesseract instalado, 'pytesseract' y 'Pillow' en tu entorno.
      - Asegurarte de que las imágenes descargadas se encuentren en:
        'downloaded_images/<nombre_de_archivo>'

    Devolverá una lista de incidencias.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # Palabras alt genéricas que NO aportan valor
    GENERIC_WORDS = {"image", "photo", "picture", "graphic", "icon", "logo"}

    for img in soup.find_all("img"):
        src_attr = img.get("src") or ""
        alt_value = img.get("alt")

        # ─────────────────────────────────────────────────────────────────
        # 1) Verificar alt vacío o ausente
        if alt_value is None or alt_value.strip() == "":
            incidences.append({
                "title": "Informative image with missing or empty alt",
                "type": "Screen Reader",
                "severity": "High",
                "description": (
                    f"The image '{src_attr}' (informative) has no or empty alt. "
                    "Screen reader users won't perceive the info.\n"
                    "Ref: https://www.w3.org/WAI/tutorials/images/informative/"
                ),
                "remediation": (
                    "Add a short, meaningful alt text that conveys the message.\n"
                    "Ej: <img src='cap.png' alt='Push the cap down and turn it counter-clockwise...'>"
                ),
                "wcag_reference": "1.1.1",
                "impact": "Essential info lost for screen readers.",
                "page_url": page_url,
            })
            continue

        alt_stripped = alt_value.strip()
        alt_lower = alt_stripped.lower()

        # ─────────────────────────────────────────────────────────────────
        # 2) Alt genérico (ej. “image”, “photo”, “icon”)
        if alt_lower in GENERIC_WORDS or alt_lower in {f"an {w}" for w in GENERIC_WORDS}:
            incidences.append({
                "title": "Informative image has a generic alt text",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    f"The image '{src_attr}' uses a generic alt '{alt_stripped}', "
                    "which doesn't convey the actual meaning.\n"
                    "Ref: https://www.w3.org/WAI/tutorials/images/informative/"
                ),
                "remediation": (
                    "Use a short phrase describing the content.\n"
                    "Ej: <img src='dog.jpg' alt='Dog with a bell attached to its collar.'>"
                ),
                "wcag_reference": "1.1.1",
                "impact": "Screen reader users get a useless label instead of real info.",
                "page_url": page_url,
            })
            # No salimos; seguimos para que OCR revise si hay texto.

        # ─────────────────────────────────────────────────────────────────
        # 3) Intentar localizar la imagen en la carpeta downloaded_images
        #    - El src puede venir ya con 'downloaded_images/...' o no. Hacemos un manejo genérico.
        image_filename = os.path.basename(src_attr)  # nombre de archivo
        local_path = os.path.join("downloaded_images", image_filename)

        # Verificar que la imagen exista en 'downloaded_images' antes de OCR
        if not os.path.isfile(local_path):
            # No hay imagen local => no OCR
            # Lo consideramos un warning opcional o simplemente lo ignoramos.
            continue

        # ─────────────────────────────────────────────────────────────────
        # 4) Ejecutar OCR
        import pytesseract

        #Ruta donde se instaló Tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        try:
            text_extracted = pytesseract.image_to_string(Image.open(local_path)).strip()
        except Exception as e:
            incidences.append({
                "title": "OCR error",
                "type": "Test Execution",
                "severity": "Medium",
                "description": f"OCR failed for '{local_path}'. Error: {e}",
                "remediation": (
                    "Check Tesseract installation or image readability."
                ),
                "wcag_reference": None,
                "impact": "No textual comparison was possible for that image.",
                "page_url": page_url,
            })
            continue

        # 5) Si se extrajo texto, comparar con alt
        if text_extracted:
            # Heurística muy simple: proporción de palabras en común.
            ocr_lower = text_extracted.lower()
            set_ocr = set(ocr_lower.split())
            set_alt = set(alt_lower.split())

            if set_ocr:  # Evitar división por cero
                intersection_count = len(set_ocr & set_alt)
                similarity = intersection_count / len(set_ocr)
            else:
                similarity = 0.0

            if similarity < 0.3:
                incidences.append({
                    "title": "Alt text may be inaccurate compared to image text",
                    "type": "Screen Reader",
                    "severity": "Medium",
                    "description": (
                        f"Image: '{local_path}'\n"
                        f"OCR text: '{text_extracted[:80]}...'\n"  # truncamos 80 caracters
                        f"Alt: '{alt_stripped}'\n"
                        f"Overlap: {similarity*100:.1f}%\n\n"
                        "Suggests the alt doesn't match essential text in the image.\n"
                        "Ref: https://www.w3.org/WAI/tutorials/images/informative/"
                    ),
                    "remediation": (
                        "Update the alt to properly reflect the text in the image (if that text is relevant)."
                    ),
                    "wcag_reference": "1.1.1",
                    "impact": (
                        "Screen reader users get an alt that doesn't match the real text in the image."
                    ),
                    "page_url": page_url,
                })

    return incidences
