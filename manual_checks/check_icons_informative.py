# manual_checks/check_icons_informative.py

from bs4 import BeautifulSoup

def check_icons_informative(html_content, page_url):
    """
    Verifica si los íconos CSS, imágenes o SVGs que transmiten información
    son accesibles para los lectores de pantalla.
    """
    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🚨 1. Detectar íconos CSS sin texto accesible
    for icon in soup.find_all(["span", "i"], class_=["icon", "fa", "material-icons"]):
        aria_hidden = icon.get("aria-hidden")
        has_text = bool(icon.text.strip())

        if aria_hidden is None or aria_hidden.lower() != "true":
            if not has_text:
                incidences.append({
                    "title": "Informative icon is not announced",
                    "type": "Screen Reader",
                    "severity": "High",
                    "description": (
                        "An informative icon is present but does not provide an accessible label. "
                        "Icons should have either an `aria-label`, `aria-labelledby`, or hidden supporting text."
                    ),
                    "remediation": (
                        "Ensure that icons conveying information are announced by screen readers.\n"
                        "Options:\n"
                        "- Use `aria-label='Active'` or `aria-labelledby`.\n"
                        "- Provide a visually hidden text element after the icon using CSS (`.sr-only`)."
                    ),
                    "wcag_reference": "1.1.1",
                    "impact": "Screen reader users will not perceive the information conveyed by the icon.",
                    "page_url": page_url,
                })

    # 🚨 2. Detectar imágenes informativas sin alt
    for img in soup.find_all("img"):
        alt = img.get("alt")
        role = img.get("role")

        if alt is None or alt.strip() == "":
            incidences.append({
                "title": "Informative image is not set as such",
                "type": "Screen Reader",
                "severity": "High",
                "description": (
                    "An image that conveys information does not have an alternative text (`alt`). "
                    "Screen reader users will not receive the intended information."
                ),
                "remediation": (
                    "Provide a meaningful `alt` attribute that describes the image.\n"
                    "Example: `<img src='error.png' alt='Error: Invalid credentials'>`."
                ),
                "wcag_reference": "1.1.1",
                "impact": "Screen readers will skip the image, preventing users from getting its information.",
                "page_url": page_url,
            })

    # 🚨 3. Detectar SVGs sin `title` o `aria-labelledby`
    for svg in soup.find_all("svg"):
        title = svg.find("title")
        aria_labelledby = svg.get("aria-labelledby")
        role = svg.get("role")

        if not title and not aria_labelledby:
            incidences.append({
                "title": "Informative SVG is not accessible",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    "An SVG that conveys information does not have a `title` element or `aria-labelledby`. "
                    "Screen readers might not recognize this as an informative graphic."
                ),
                "remediation": (
                    "Ensure the SVG has an accessible name by using:\n"
                    "- A `<title>` element inside the `<svg>`.\n"
                    "- The `aria-labelledby` attribute referencing the `<title>`.\n"
                    "Example:\n"
                    "<svg aria-labelledby='svg-title'><title id='svg-title'>Active event</title></svg>"
                ),
                "wcag_reference": "1.1.1",
                "impact": "Users with screen readers will miss the visual information conveyed by the SVG.",
                "page_url": page_url,
            })

    return incidences
