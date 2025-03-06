from bs4 import BeautifulSoup

def check_name_role_value(html_content, page_url):
    """
    Analiza el HTML en busca de componentes de interfaz que no tengan nombre, rol o valor accesible.
    Basado en WCAG 4.1.2 (Name, Role, Value, Nivel A).

    Parámetros:
    - html_content (str): Código HTML de la página.
    - page_url (str): URL o ruta del archivo analizado.

    Retorna:
    - Lista de incidencias detectadas.
    """

    soup = BeautifulSoup(html_content, 'html.parser')
    incidencias = []

    # Buscar elementos interactivos sin accesibilidad adecuada
    interactive_elements = soup.find_all(["button", "input", "textarea", "select", "a", "div", "span"])

    for element in interactive_elements:
        element_id = element.get("id") or element.get("name") or "elemento sin ID"

        # 1️⃣ Verificar si tiene un nombre accesible
        has_name = element.get_text(strip=True) or element.get("aria-label") or element.get("aria-labelledby")
        if not has_name:
            incidencias.append({
                "page_url": page_url,
                "issue": "Falta de nombre accesible",
                "description": f"El elemento '{element.name}' con ID '{element_id}' no tiene un nombre accesible.",
                "wcag_reference": "4.1.2 (Name, Role, Value, Nivel A)",
                "severity": "high",
                "suggested_fix": "Agregar un 'aria-label' o 'aria-labelledby' o contenido textual."
            })

        # 2️⃣ Verificar si tiene un rol definido cuando es necesario
        if element.name in ["div", "span"] and not element.get("role"):
            incidencias.append({
                "page_url": page_url,
                "issue": "Falta de rol accesible",
                "description": f"El elemento '{element.name}' con ID '{element_id}' no tiene un rol definido.",
                "wcag_reference": "4.1.2 (Name, Role, Value, Nivel A)",
                "severity": "medium",
                "suggested_fix": "Añadir un atributo 'role' adecuado (ejemplo: role='button')."
            })

        # 3️⃣ Verificar si tiene estado/valor programático
        if element.name == "input" and element.get("type") in ["checkbox", "radio"]:
            if "aria-checked" not in element.attrs and "checked" not in element.attrs:
                incidencias.append({
                    "page_url": page_url,
                    "issue": "Falta de valor accesible",
                    "description": f"El checkbox/radio '{element_id}' no tiene un estado programáticamente determinado.",
                    "wcag_reference": "4.1.2 (Name, Role, Value, Nivel A)",
                    "severity": "high",
                    "suggested_fix": "Agregar 'aria-checked' para indicar el estado del checkbox/radio."
                })

    return incidencias
