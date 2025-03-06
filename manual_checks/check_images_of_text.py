from bs4 import BeautifulSoup, NavigableString
import os
import pytesseract
from PIL import Image

def check_images_of_text(html_content, page_url, images_folder="downloaded_images"):
    """
    Verifica si las imágenes contienen texto (OCR) y, si es así, revisa si
    hay texto real cercano que coincida.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue

        filename = os.path.basename(src)
        local_path = os.path.join(images_folder, filename)

        if not os.path.isfile(local_path):
            # No se hace OCR si no existe la imagen local.
            continue
        
        # OCR
        try:
            text_extracted = pytesseract.image_to_string(Image.open(local_path)).strip()
        except Exception as e:
            incidences.append({
                "title": "OCR error",
                "description": f"OCR failed for {src}: {e}",
                "page_url": page_url
            })
            continue
        
        # Si encontramos texto en la imagen
        if text_extracted:
            # Revisar alt
            alt_value = img.get("alt", "")

            # Tomar solo nodos de texto (NavigableString) en los siblings
            sibling_text_nodes = []
            for sibling in img.next_siblings:
                # Filtrar solo los nodos de texto
                if isinstance(sibling, NavigableString):
                    sibling_text_nodes.append(str(sibling))

            sibling_text = "".join(sibling_text_nodes)

            # Comprobamos si el texto extraído no está incluido en alt + texto cercano
            combined_text = (alt_value + sibling_text).lower()
            if text_extracted.lower() not in combined_text:
                incidences.append({
                    "title": "Image of Text Possibly Used",
                    "page_url": page_url,
                    "description": (
                        f"La imagen '{src}' contiene texto (OCR): '{text_extracted[:60]}...' "
                        "pero el HTML no presenta texto equivalente. Esto sugiere uso de imagen de texto "
                        "sin versión textual real.\n"
                        "Refer to WCAG 1.4.5: Images of Text."
                    ),
                    "recommendation": (
                        "Implementar el texto en HTML real o usar la Technique C30 para permitirle al usuario "
                        "conmutar a una versión solo texto."
                    )
                })

    return incidences
