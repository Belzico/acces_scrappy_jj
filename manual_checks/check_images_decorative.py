# manual_checks/check_images_decorative.py

from bs4 import BeautifulSoup

def check_images_decorative(html_content, page_url):
    """
    Verifica imágenes y elementos decorativos para asegurar que están correctamente ocultos 
    a los lectores de pantalla y teclados, y que no tienen atributos incorrectos.
    """
    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    for img in soup.find_all("img"):
        src_value = img.get("src", "")
        alt_value = img.get("alt")
        aria_hidden = img.get("aria-hidden")
        role = img.get("role")
        tabindex = img.get("tabindex")

        # 🚨 1. IMAGEN SIN ALT (Error: Debe ser alt="" o un texto descriptivo)
        if alt_value is None:
            incidences.append({
                "title": "Missing alt attribute",
                "type": "Screen Reader",
                "severity": "High",
                "description": (
                    f"The image '{src_value}' does not have an 'alt' attribute. "
                    "All images must have an 'alt' attribute, either empty (alt=\"\") for decorative images "
                    "or descriptive for informative images."
                ),
                "remediation": (
                    "Ensure that all images have an 'alt' attribute.\n"
                    "Use alt=\"\" for purely decorative images or provide a meaningful description."
                ),
                "wcag_reference": "1.1.1",
                "impact": "Screen readers will announce 'image' without any description, confusing users.",
                "page_url": page_url,
            })

        # 🚨 2. IMAGEN DECORATIVA QUE ES ENFOCADA Y ANUNCIADA
        elif alt_value.strip() == "" and (aria_hidden is None or aria_hidden.lower() != "true") and tabindex not in ["-1"]:
            incidences.append({
                "title": "Decorative image is focused and announced",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    f"The image '{src_value}' is decorative (has alt=\"\"), "
                    "but it is still announced by screen readers because it lacks aria-hidden=\"true\" "
                    "or is focusable using keyboard navigation."
                ),
                "remediation": (
                    "Add aria-hidden=\"true\" or role=\"presentation\" to hide this image from assistive technologies.\n"
                    "If it is getting focus, set tabindex=\"-1\"."
                ),
                "wcag_reference": "1.1.1",
                "impact": "Screen readers will focus the image, slowing down user navigation.",
                "page_url": page_url,
            })

        # 🚨 3. IMAGEN DECORATIVA CON TEXTO ALT INCORRECTO
        elif alt_value.strip() != "" and "decorative" in src_value.lower():
            incidences.append({
                "title": "Decorative image has incorrect alt",
                "type": "Other A11y",
                "severity": "Medium",
                "description": (
                    f"The image '{src_value}' is likely decorative but has an alt text: '{alt_value}'.\n"
                    "Decorative images should have an empty alt attribute (alt=\"\")."
                ),
                "remediation": (
                    "Remove the text inside the 'alt' attribute.\n"
                    "Use alt=\"\" to indicate that this image is purely decorative."
                ),
                "wcag_reference": "1.1.1",
                "impact": "Screen readers will announce unnecessary content, disrupting navigation.",
                "page_url": page_url,
            })

    # 🚨 4. DETECTAR SEPARADORES <hr>, <svg> SIN aria-hidden="true"
    for element in soup.find_all(["hr", "svg"]):
        aria_hidden = element.get("aria-hidden")
        role = element.get("role")
        tabindex = element.get("tabindex")

        if aria_hidden is None and role not in ["presentation", "none"] and tabindex not in ["-1"]:
            incidences.append({
                "title": "Decorative separator is focused and announced",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    f"A decorative element ('{element.name}') is visible to screen readers but should be hidden.\n"
                    "It should have aria-hidden=\"true\" or role=\"presentation\", and should not be focusable."
                ),
                "remediation": (
                    "Add aria-hidden=\"true\" or role=\"presentation\" to this element.\n"
                    "If it is getting focus, set tabindex=\"-1\"."
                ),
                "wcag_reference": "1.1.1",
                "impact": "Decorative elements being announced can make finding real content more difficult.",
                "page_url": page_url,
            })

    return incidences
