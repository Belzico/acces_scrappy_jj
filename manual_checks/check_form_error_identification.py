from bs4 import BeautifulSoup

def check_form_error_identification(html_content, page_url):
    """
    Analiza el HTML en busca de errores de formulario que no están identificados correctamente en texto,
    en conformidad con WCAG 3.3.1 (Error Identification, Nivel A).
    
    Parámetros:
    - html_content (str): Código HTML de la página.
    - page_url (str): URL o ruta del archivo analizado.

    Retorna:
    - Lista de incidencias detectadas.
    """

    # Asegurar que BeautifulSoup pueda manejar HTML mal formado
    soup = BeautifulSoup(html_content, 'html.parser')

    incidencias = []

    # Intenta encontrar campos con `aria-invalid="true"` asegurando case insensitivity
    error_fields = soup.find_all(lambda tag: 
        tag.name in ["input", "textarea", "select"] and 
        tag.has_attr("aria-invalid") and 
        tag["aria-invalid"].lower() == "true"
    )

    if not error_fields:
        print("⚠️ No se encontraron campos con aria-invalid='true' en la página:", page_url)
        return incidencias  # Retornar vacío si no hay errores detectados

    for field in error_fields:
        field_name = field.get("name") or field.get("id") or "campo sin nombre"
        error_text = None  # Reiniciamos el error_text en cada iteración

        # 1️⃣ Si el input tiene aria-describedby, verificamos ese mensaje exclusivamente
        described_by = field.get("aria-describedby")
        if described_by:
            described_error = soup.find(id=described_by)
            if described_error and described_error.get_text(strip=True):
                # Verificar si el mensaje está oculto
                if not described_error.has_attr("style") or "display: none" not in described_error["style"]:
                    error_text = described_error.get_text(strip=True)

        # 2️⃣ Si no tiene aria-describedby, buscar el mensaje de error en la siguiente etiqueta adyacente directa
        if not error_text:
            next_sibling = field.find_next_sibling()
            while next_sibling:
                if next_sibling.name in ["span", "div", "p", "small"] and "error" in " ".join(next_sibling.get("class", [])):
                    if not next_sibling.has_attr("style") or "display: none" not in next_sibling["style"]:
                        error_text = next_sibling.get_text(strip=True)
                        break  # Solo tomamos el primer mensaje válido asociado
                next_sibling = next_sibling.find_next_sibling()

        # 3️⃣ Si no se encontró un mensaje de error en texto visible, se genera una incidencia
        if not error_text:
            incidencias.append({
                "page_url": page_url,
                "issue": "Falta mensaje de error en texto",
                "description": f"El campo '{field_name}' está marcado como inválido pero no tiene un mensaje de error visible.",
                "wcag_reference": "3.3.1 (Error Identification, Nivel A)",
                "severity": "high",
                "suggested_fix": "Añadir un mensaje de error en texto visible cerca del campo o enlazado con aria-describedby."
            })

    return incidencias
