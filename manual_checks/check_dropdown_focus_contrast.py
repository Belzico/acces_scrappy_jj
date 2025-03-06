import re
from bs4 import BeautifulSoup

# --- Funciones de ayuda para color y contraste ---

def luminance(color_hex):
    """
    Calcula la luminancia relativa de un color en formato HEX o rgb() o rgba().
    Devuelve un valor entre 0 y 1.
    """
    # Normalizamos siempre a hex de 6 dígitos (sin #) para simplificar,
    # a menos que sea rgb() o rgba().
    color_hex = color_hex.strip().lower()

    # Si es rgb(...) o rgba(...):
    if color_hex.startswith("rgb"):
        # Extraer los valores entre paréntesis, ejemplo: "rgb(241, 244, 244)"
        # o "rgba(241, 244, 244, 0.5)"
        nums_str = color_hex[color_hex.index("(")+1 : color_hex.index(")")]
        vals = [x.strip() for x in nums_str.split(",")]
        # Los tres primeros siempre son R, G, B
        r = float(vals[0])
        g = float(vals[1])
        b = float(vals[2])

        # Si es 0..255, escalamos a [0..1]
        r /= 255.0
        g /= 255.0
        b /= 255.0

    else:
        # Es un formato #xxx o #xxxxxx
        if color_hex.startswith("#"):
            color_hex = color_hex[1:]  # quitamos '#'
        if len(color_hex) == 3:
            # Expandir #abc => #aabbcc
            color_hex = "".join([ch*2 for ch in color_hex])
        # Extraer r,g,b en [0..1]
        r = int(color_hex[0:2], 16) / 255.0
        g = int(color_hex[2:4], 16) / 255.0
        b = int(color_hex[4:6], 16) / 255.0

    # Convertimos cada componente con la fórmula sRGB:
    def srgb_to_linear(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r_lin = srgb_to_linear(r)
    g_lin = srgb_to_linear(g)
    b_lin = srgb_to_linear(b)

    # Luminancia relativa (WCAG)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

def contrast_ratio(color1, color2):
    lum1 = luminance(color1)
    lum2 = luminance(color2)
    lighter = max(lum1, lum2)
    darker  = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)

# --- Parser básico de reglas CSS internas ---

def extract_css_colors(html_content):
    """
    Busca reglas CSS dentro de <style> y devuelve un diccionario
    con las propiedades encontradas para ciertos selectores, por ejemplo:
    
    {
      'option:hover':    {'color': '#000000', 'background': '#f1f4f4'},
      'option[selected]':{'color': '#000', 'background': '#fff'},
      ...
    }
    """
    soup = BeautifulSoup(html_content, "html.parser")
    styles = soup.find_all("style")

    css_rules = {}

    # Regex para capturar color y background (hex 3/6 dígitos, rgb, rgba)
    color_regex = re.compile(
        r'color:\s*(#[0-9A-Fa-f]{3,6}|rgb\([^)]+\)|rgba\([^)]+\))',
        re.IGNORECASE
    )
    bg_regex = re.compile(
        r'background(?:-color)?:\s*(#[0-9A-Fa-f]{3,6}|rgb\([^)]+\)|rgba\([^)]+\))',
        re.IGNORECASE
    )

    for style_tag in styles:
        # Obtenemos el texto completo dentro de <style>...</style>
        style_content = style_tag.get_text()

        # Separamos por "}" para aislar cada bloque de reglas
        blocks = style_content.split("}")

        for block in blocks:
            block = block.strip()
            if not block:
                continue
            # Cada bloque debería tener "selector { propiedades..."
            parts = block.split("{", 1)
            if len(parts) != 2:
                continue

            selector_part = parts[0].strip()
            props_part    = parts[1].strip()

            # Buscamos color y background
            color_match = color_regex.search(props_part)
            bg_match    = bg_regex.search(props_part)

            found_color = color_match.group(1) if color_match else None
            found_bg    = bg_match.group(1) if bg_match else None

            # Puede que el selector tenga comas (ej: "option:hover, option:focus")
            # Dividimos cada uno y guardamos individualmente
            multiple_selectors = [s.strip() for s in selector_part.split(",")]

            for sel in multiple_selectors:
                # Normalizamos: "option:hover", "option:focus", etc.
                if found_color or found_bg:
                    # Si ya existe, actualizamos (por si hay varias props)
                    if sel not in css_rules:
                        css_rules[sel] = {}

                    if found_color:
                        css_rules[sel]["color"] = found_color
                    if found_bg:
                        css_rules[sel]["background"] = found_bg

    return css_rules

# --- Función principal de chequeo ---

def check_dropdown_focus_contrast(html_content, page_url):
    """
    Verifica si las opciones seleccionadas o enfocadas en un dropdown tienen suficiente contraste (>= 3:1).
    
    - Busca <select> en toda la página.
    - Para cada <option>, si está seleccionado (HTML) o si queremos simular 'hover',
      se revisa si hay una regla en CSS que aplique (p.ej. "option[selected]", "option:hover").
    - Calcula la relación de contraste y reporta si es menor a 3:1.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    css_styles = extract_css_colors(html_content)
    dropdowns = soup.find_all("select")

    incidencias = []

    for dropdown in dropdowns:
        all_options = dropdown.find_all("option")

        for option in all_options:
            # Determinar si <option> está seleccionado en HTML
            is_selected = option.has_attr("selected")

            # Vamos a “simular” que también nos interesa la regla de :hover (o :focus)
            # Ojo: Esto es una suposición, en la práctica el :hover no se ve en HTML estático
            # pero lo hacemos para ejemplificar.
            states_to_test = []
            if is_selected:
                states_to_test.append("selected")
            # Descomenta si quieres forzar también hover/focus:
            # states_to_test.append("hover")
            # states_to_test.append("focus")

            for state in states_to_test:
                # Construimos el selector tal cual lo guardamos en css_rules
                # por ejemplo: "option[selected]" o "option:hover"
                selector_key = f"option:{state}" if state in ["hover", "focus"] else f"option[{state}]"

                # Buscamos si hay una regla en css_styles que coincida con EXACTAMENTE ese selector
                # o si hay algo como "option:hover, option:focus".
                # Para simplificar, si no existe la clave exacta, probamos a ver si algún selector
                # contuviera esa parte. (Por ejemplo, "option:hover, option:focus")
                matched_rule = css_styles.get(selector_key)

                if not matched_rule:
                    # Revisa también selectores “compuestos”
                    for k in css_styles:
                        # ejemplo "option:hover, option:focus"
                        if selector_key in k.replace(" ", ""):  # algo rudimentario
                            matched_rule = css_styles[k]
                            break

                # Asignar colores finales (si no hay en CSS, usar colores por defecto)
                text_color = matched_rule.get("color", "#000") if matched_rule else "#000"
                bg_color   = matched_rule.get("background", "#fff") if matched_rule else "#fff"

                # Calculamos contraste
                ratio = contrast_ratio(text_color, bg_color)

                if ratio < 3.0:
                    incidencias.append({
                        "title": "Dropdown selected/hovered option fails color contrast requirements",
                        "type": "Color Contrast",
                        "severity": "High",
                        "description": (
                            f"La opción (estado {state}) en el dropdown tiene un contraste de {ratio:.2f}:1, "
                            "por debajo del mínimo 3:1 recomendado para estados activos."
                        ),
                        "remediation": (
                            "Usar un color más oscuro para el fondo o un color de texto más claro. "
                            "Por ejemplo: background-color: #939393;"
                        ),
                        "wcag_reference": "1.4.11",
                        "impact": (
                            "Los usuarios con baja visión pueden no notar qué opción está seleccionada o "
                            "enfocada si el contraste es insuficiente."
                        ),
                        "page_url": page_url,
                        "affected_element": str(option)
                    })

    return incidencias
