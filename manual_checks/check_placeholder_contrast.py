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

# Función principal para detectar problemas de contraste en placeholders
def check_placeholder_contrast(html_content, page_url):
    """
    Verifica si el texto del placeholder en los campos `<input>` tiene suficiente contraste con el fondo.

    - Busca `<input>` con atributo `placeholder`.
    - Obtiene los colores del texto y del fondo (si están en `style` o valores por defecto).
    - Calcula la relación de contraste y reporta si es menor a 4.5:1.
    """

    soup = BeautifulSoup(html_content, "html.parser")

    # Buscar todos los inputs con placeholder
    inputs = soup.find_all("input", attrs={"placeholder": True})

    incidencias = []
    for input_field in inputs:
        # Obtener el color del placeholder y el fondo desde el atributo style si existen
        text_color_match = re.search(r'color:\s*(#[0-9A-Fa-f]{6})', input_field.get("style", ""))
        bg_color_match = re.search(r'background-color:\s*(#[0-9A-Fa-f]{6})', input_field.get("style", ""))

        # Si no hay color especificado, asumir valores por defecto
        text_color = text_color_match.group(1) if text_color_match else "#BFCAD1"  # Placeholder gris claro
        bg_color = bg_color_match.group(1) if bg_color_match else "#FFFFFF"  # Fondo blanco

        # Calcular relación de contraste
        contrast = contrast_ratio(text_color, bg_color)

        if contrast < 4.5:
            incidencias.append({
                "title": "Grey placeholder fails contrast on white background",
                "type": "Color Contrast",
                "severity": "High",
                "description": (
                    f"El placeholder en el campo de entrada tiene un contraste de {contrast:.2f}:1, "
                    "lo que no cumple con el mínimo de 4.5:1 recomendado para texto pequeño."
                ),
                "remediation": (
                    "Usar un color más oscuro para el texto del placeholder o cambiar el fondo a un color con mayor contraste. "
                    "Ejemplo: `color: #757575;` en lugar de `color: #BFCAD1;`."
                ),
                "wcag_reference": "1.4.3",
                "impact": "Los usuarios con baja visión no podrán leer el texto del placeholder.",
                "page_url": page_url,
                "affected_element": str(input_field)
            })

    return incidencias
