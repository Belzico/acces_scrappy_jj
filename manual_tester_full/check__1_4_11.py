import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

# --- Funciones de ayuda para líneas de HTML y snippet ---
def get_html_lines(html_content):
    """
    Dado el HTML como string, lo dividimos por líneas.
    Útil para luego extraer un snippet alrededor de line_number.
    """
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    lines: lista de líneas del HTML (salida de get_html_lines)
    line_number: número de línea (base 1) donde se encontró el elemento
    context: cuántas líneas antes y después extraer

    Retorna un string con el fragmento de HTML alrededor de esa línea.
    """
    idx = line_number - 1  # Ajuste a base 0
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]

    # Para mostrar con numeración real
    snippet_str = "\n".join(
        f"{i+1}: {snippet[i - start]}"
        for i in range(start, end)
    )
    return snippet_str

# --- Funciones de ayuda para color y contraste ---
def luminance(color_hex):
    color_hex = color_hex.strip().lower()

    if color_hex.startswith("rgb"):
        nums_str = color_hex[color_hex.index("(") + 1 : color_hex.index(")")]
        vals = [x.strip() for x in nums_str.split(",")]
        r = float(vals[0]) / 255.0
        g = float(vals[1]) / 255.0
        b = float(vals[2]) / 255.0
    else:
        if color_hex.startswith("#"):
            color_hex = color_hex[1:]
        if len(color_hex) == 3:
            color_hex = "".join([ch * 2 for ch in color_hex])
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
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)

# --- Función para extraer reglas CSS de color y background ---
def extract_css_colors(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    styles = soup.find_all("style")
    css_rules = {}

    color_regex = re.compile(r'color:\s*(#[0-9A-Fa-f]{3,6}|rgb\([^)]+\)|rgba\([^)]+\))', re.IGNORECASE)
    bg_regex = re.compile(r'background(?:-color)?:\s*(#[0-9A-Fa-f]{3,6}|rgb\([^)]+\)|rgba\([^)]+\))', re.IGNORECASE)

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

# --- Nueva versión de get_element_info para incluir snippet ---
def get_element_info(element, html_lines=None):
    """
    Devuelve información detallada del elemento HTML para el reporte,
    incluyendo un snippet (fragment_html) alrededor de la línea donde se encontró.
    """
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    evidence_parts = []
    if classes:
        evidence_parts.append(f"class={classes}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")

    evidence_str = ", ".join(evidence_parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_str else tag

    # Extraer snippet de HTML alrededor de line_number
    snippet_str = ""
    if line_number != "N/A" and html_lines:
        try:
            line_int = int(line_number)
            snippet_str = get_line_snippet(html_lines, line_int, context=2)
        except ValueError:
            pass

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence,
        "fragment_html": snippet_str  # <-- Agregamos el snippet
    }

# --- Formateo final de la incidencia con snippet ---
def format_incidence(old):
    """
    Formatea la incidencia para el reporte. Incluye snippet de HTML en 'Steps'.
    """
    element_info = old.get("element_info", {})
    snippet = element_info.get("fragment_html", "")
    line_number = element_info.get("line_number", "N/A")

    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Abrir la página: {old.get('page_url')}\n"
            f"2. Inspeccionar el elemento: {element_info.get('tag', 'N/A')}\n"
            f"3. Verificar el contraste entre texto y fondo en estado activo/enfocado.\n\n"
            f"Fragmento de HTML (alrededor de la línea {line_number}):\n"
            f"{snippet}"
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("expected_result", "N/A"),
        "Actual Result": old.get("actual_result", "N/A"),
        "Suggested resolution(s)": old.get("remediation"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact", "N/A"),
        "Evidence [SS or Video]": element_info.get("evidence", "N/A")
    }

def run_all___1_4_11(html_content, page_url, excel="issue_report.xlsx"):
    """
    Evalúa si las opciones de un <select> en estado activo o enfocado cumplen con el
    contraste mínimo (3:1), según WCAG 1.4.11.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    css_styles = extract_css_colors(html_content)
    dropdowns = soup.find_all("select")

    # Obtenemos las líneas de HTML para extraer snippets
    html_lines = get_html_lines(html_content)

    raw_incidences = []

    for dropdown in dropdowns:
        all_options = dropdown.find_all("option")

        for option in all_options:
            is_selected = option.has_attr("selected")
            states_to_test = ["selected"] if is_selected else []

            for state in states_to_test:
                # Para matchear algo como "option:selected" en CSS
                selector_key = f"option:{state}" if state in ["hover", "focus"] else f"option[{state}]"
                matched_rule = css_styles.get(selector_key)

                if not matched_rule:
                    # Buscar si hay una regla que contenga la parte "option:selected" en su selector
                    for k in css_styles:
                        if selector_key in k.replace(" ", ""):
                            matched_rule = css_styles[k]
                            break

                text_color = matched_rule.get("color", "#000") if matched_rule else "#000"
                bg_color = matched_rule.get("background", "#fff") if matched_rule else "#fff"

                ratio = contrast_ratio(text_color, bg_color)

                if ratio < 3.0:
                    raw_incidences.append({
                        "title": "Opción seleccionada del dropdown con contraste insuficiente",
                        "type": "Color Contrast",
                        "severity": "High",
                        "expected_result": "La opción seleccionada o enfocada debe tener un contraste mínimo de 3:1.",
                        "actual_result": f"La opción del dropdown tiene un contraste de {ratio:.2f}:1.",
                        "remediation": (
                            "Usar un color de fondo más oscuro o un color de texto más claro. "
                            "Por ejemplo: `background-color: #939393;`."
                        ),
                        "wcag_reference": "1.4.11",
                        "impact": (
                            "Los usuarios con baja visión podrían no notar cuál opción está seleccionada o enfocada "
                            "si el contraste es insuficiente."
                        ),
                        "page_url": page_url,
                        # Pasamos html_lines para el snippet
                        "element_info": get_element_info(option, html_lines=html_lines)
                    })

    formatted = [format_incidence(inc) for inc in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)
    return formatted
