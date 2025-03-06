from bs4 import BeautifulSoup
import re

# Función para calcular la luminancia relativa de un color
def luminance(color):
    r, g, b = [int(color[i:i+2], 16) / 255.0 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return (0.2126 * rgb[0]) + (0.7152 * rgb[1]) + (0.0722 * rgb[2])

# Función para calcular la relación de contraste entre dos colores
def contrast_ratio(color1, color2):
    lum1, lum2 = luminance(color1), luminance(color2)
    return (max(lum1, lum2) + 0.05) / (min(lum1, lum2) + 0.05)

# Función principal para detectar problemas de contraste en dropdowns
def check_dropdown_contrast(html_content, page_url):
    """
    Verifica si las opciones seleccionadas en los dropdowns tienen suficiente contraste con el fondo.
    
    - Busca `<select>` y sus opciones seleccionadas `<option selected>`.
    - Si no hay `selected`, usa la primera opción visible.
    - Obtiene los colores del texto y fondo (si están en `style` o por defecto).
    - Calcula la relación de contraste y reporta si es menor a 4.5:1.
    """

    soup = BeautifulSoup(html_content, "html.parser")

    # Buscar todos los <select> en la página
    dropdowns = soup.find_all("select")

    incidencias = []
    for dropdown in dropdowns:
        # Obtener la opción seleccionada
        selected_option = dropdown.find("option", selected=True) or dropdown.find("option")

        if selected_option:
            # Obtener el color del texto y el fondo desde el atributo style si existen
            text_color_match = re.search(r'color:\s*(#[0-9A-Fa-f]{6})', selected_option.get("style", ""))
            bg_color_match = re.search(r'background-color:\s*(#[0-9A-Fa-f]{6})', selected_option.get("style", ""))

            # Si no hay color especificado, asumir valores por defecto
            text_color = text_color_match.group(1) if text_color_match else "#000000"  # Negro por defecto
            bg_color = bg_color_match.group(1) if bg_color_match else "#FFFFFF"  # Blanco por defecto

            # Calcular relación de contraste
            contrast = contrast_ratio(text_color, bg_color)

            if contrast < 4.5:
                incidencias.append({
                    "title": "Dropdown selected value fails contrast once expanded",
                    "type": "Color Contrast",
                    "severity": "High",
                    "description": (
                        f"La opción seleccionada en el dropdown tiene un contraste de {contrast:.2f}:1, "
                        "lo que no cumple con el mínimo de 4.5:1 recomendado para texto pequeño."
                    ),
                    "remediation": (
                        "Usar un color más oscuro para el texto o cambiar el fondo a un color con mayor contraste. "
                        "Ejemplo: `color: #2C3E50;` en lugar de `color: #BAC7CB;`."
                    ),
                    "wcag_reference": "1.4.3",
                    "impact": "Los usuarios con baja visión no podrán leer el texto de la opción seleccionada.",
                    "page_url": page_url,
                    "affected_element": str(selected_option)
                })

    return incidencias
