import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

# --- Funciones de ayuda para color y contraste ---

def luminance(color_hex):
    """
    Calcula la luminancia relativa de un color en formato HEX o rgb() o rgba().
    Devuelve un valor entre 0 y 1.
    """
    color_hex = color_hex.strip().lower()

    if color_hex.startswith("rgb"):
        nums_str = color_hex[color_hex.index("(")+1 : color_hex.index(")")]
        vals = [x.strip() for x in nums_str.split(",")]
        r = float(vals[0]) / 255.0
        g = float(vals[1]) / 255.0
        b = float(vals[2]) / 255.0
    else:
        if color_hex.startswith("#"):
            color_hex = color_hex[1:]
        if len(color_hex) == 3:
            color_hex = "".join([ch*2 for ch in color_hex])
        r = int(color_hex[0:2], 16) / 255.0
        g = int(color_hex[2:4], 16) / 255.0
        b = int(color_hex[4:6], 16) / 255.0

    def srgb_to_linear(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r_lin = srgb_to_linear(r)
    g_lin = srgb_to_linear(g)
    b_lin = srgb_to_linear(b)

    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

def contrast_ratio(color1, color2):
    lum1 = luminance(color1)
    lum2 = luminance(color2)
    lighter = max(lum1, lum2)
    darker  = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)

# --- Parser de reglas CSS internas ---

def extract_css_colors(html_content):
    """
    Extrae reglas CSS dentro de <style> y devuelve un diccionario con selectores y propiedades de color.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    styles = soup.find_all("style")

    css_rules = {}

    color_regex = re.compile(
        r'color:\s*(#[0-9A-Fa-f]{3,6}|rgb\([^)]+\)|rgba\([^)]+\))',
        re.IGNORECASE
    )
    bg_regex = re.compile(
        r'background(?:-color)?:\s*(#[0-9A-Fa-f]{3,6}|rgb\([^)]+\)|rgba\([^)]+\))',
        re.IGNORECASE
    )

    for style_tag in styles:
        style_content = style_tag.get_text()
        blocks = style_content.split("}")

        for block in blocks:
            block = block.strip()
            if not block:
                continue
            parts = block.split("{", 1)
            if len(parts) != 2:
                continue

            selector_part = parts[0].strip()
            props_part = parts[1].strip()

            color_match = color_regex.search(props_part)
            bg_match = bg_regex.search(props_part)

            found_color = color_match.group(1) if color_match else None
            found_bg = bg_match.group(1) if bg_match else None

            multiple_selectors = [s.strip() for s in selector_part.split(",")]

            for sel in multiple_selectors:
                if found_color or found_bg:
                    if sel not in css_rules:
                        css_rules[sel] = {}

                    if found_color:
                        css_rules[sel]["color"] = found_color
                    if found_bg:
                        css_rules[sel]["background"] = found_bg

    return css_rules

# --- Función principal de chequeo ---

def check_dropdown_focus_contrast(html_content, page_url, excel="issue_report.xlsx"):
    """
    Verifica si las opciones seleccionadas o enfocadas en un dropdown tienen suficiente contraste (>= 3:1).
    
    - Busca <select> en toda la página.
    - Para cada <option>, revisa si hay reglas CSS aplicables a estados como `:selected`, `:hover`, `:focus`.
    - Calcula la relación de contraste y reporta si es menor a 3:1.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    css_styles = extract_css_colors(html_content)
    dropdowns = soup.find_all("select")

    incidences = []

    for dropdown in dropdowns:
        all_options = dropdown.find_all("option")

        for option in all_options:
            is_selected = option.has_attr("selected")
            states_to_test = ["selected"] if is_selected else []

            for state in states_to_test:
                selector_key = f"option:{state}" if state in ["hover", "focus"] else f"option[{state}]"
                matched_rule = css_styles.get(selector_key)

                if not matched_rule:
                    for k in css_styles:
                        if selector_key in k.replace(" ", ""):
                            matched_rule = css_styles[k]
                            break

                text_color = matched_rule.get("color", "#000") if matched_rule else "#000"
                bg_color = matched_rule.get("background", "#fff") if matched_rule else "#fff"

                ratio = contrast_ratio(text_color, bg_color)

                if ratio < 3.0:
                    incidences.append({
                        "title": "Dropdown selected/hovered option fails color contrast requirements",
                        "type": "Color Contrast",
                        "severity": "High",
                        "description": (
                            f"The dropdown option (state {state}) has a contrast ratio of {ratio:.2f}:1, "
                            "which is below the recommended minimum of 3:1 for active states."
                        ),
                        "remediation": (
                            "Use a darker background color or a lighter text color. "
                            "For example: `background-color: #939393;`."
                        ),
                        "wcag_reference": "1.4.11",
                        "impact": (
                            "Users with low vision may not notice which option is selected or focused "
                            "if the contrast is insufficient."
                        ),
                        "page_url": page_url,
                        "resolution": "check_dropdown_focus_contrast.md",
                        "affected_element": str(option)
                    })

    # Convertir incidencias a Excel antes de retornar
    transform_json_to_excel(incidences, excel)

    return incidences
