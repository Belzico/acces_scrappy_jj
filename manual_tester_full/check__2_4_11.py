import re
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_html_lines(html_content):
    """
    Dado el HTML como string, lo dividimos por líneas.
    Útil para luego extraer un snippet alrededor de line_number.
    """
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    lines: lista de líneas del HTML (output de get_html_lines)
    line_number: número de línea (base 1) donde se encontró el elemento
    context: cuántas líneas antes y después extraer

    Retorna un string con el fragmento de HTML alrededor de esa línea.
    """
    idx = line_number - 1  # ajustamos a base 0
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]

    snippet_str = "\n".join(
        f"{i+1}: {snippet[i - start]}"
        for i in range(start, end)
    )
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Construye info básica (tag, id, class, line, etc.) para evidencia,
    e incluye un fragmento HTML alrededor de esa línea.
    """
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    parts = []
    if classes:
        parts.append(f"class={classes}")
    if element_id:
        parts.append(f"id={element_id}")
    if line_number != "N/A":
        parts.append(f"line={line_number}")

    evidence_str = ", ".join(parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_str else tag

    # Extraemos el snippet del HTML si hay una línea válida y tenemos lines
    snippet_str = ""
    if line_number != "N/A" and html_lines:
        try:
            line_int = int(line_number)
            snippet_str = get_line_snippet(html_lines, line_int, context=2)
        except ValueError:
            pass

    return {
        "tag": tag,
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence,
        "fragment_html": snippet_str
    }

def format_incidence(raw_inc):
    """
    Convierte un dict en incidencia formateada para Excel,
    incluyendo el snippet HTML.
    """
    element_info = raw_inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")

    return {
        "Title": raw_inc.get("title"),
        "Steps": (
            f"1. Open the page: {raw_inc.get('page_url')}\n"
            f"2. Inspect the element: {element_info.get('tag', 'N/A')}\n"
            f"3. Verify the focus isn't completely hidden by fixed/sticky overlays.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n"
            f"{snippet}"
        ),
        "Bug Type": raw_inc.get("type"),
        "Priority": raw_inc.get("severity"),
        "Expected Result": raw_inc.get("expected_result", "N/A"),
        "Actual Result": raw_inc.get("actual_result", "N/A"),
        "Suggested resolution(s)": raw_inc.get("remediation", "N/A"),
        "Failed checkpoint": raw_inc.get("wcag_reference", "2.4.11"),
        "User Impact": raw_inc.get("impact", "N/A"),
        "Evidence [SS or Video]": element_info.get("evidence", "N/A")
    }

def parse_style_blocks_for_selectors(soup):
    """
    Analiza los <style> para detectar:
      - position: fixed/sticky
      - z-index (>= 9999)
      - height=100% / width=100%
      - height=(\\d+)px
      - covers-edge=0 (top|left|right|bottom=0)

    Devuelve un dict: { selector: set(indicadores) }.
    Ej: { '.sticky-header': {'position=fixed','heightPX=150','top=0'} }
    """
    css_findings = {}
    style_tags = soup.find_all("style")

    for style_tag in style_tags:
        css_text = style_tag.get_text()
        blocks = css_text.split("}")
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            parts = block.split("{", 1)
            if len(parts) != 2:
                continue

            selectors_part = parts[0].strip()
            styles_part = parts[1].strip().lower()

            # Buscamos patrones
            indicators = set()

            # 1) position
            pos_match = re.search(r'position\s*:\s*(fixed|sticky)', styles_part)
            if pos_match:
                indicators.add(f"position={pos_match.group(1)}")

            # 2) z-index
            z_m = re.search(r'z-index\s*:\s*(\d+)', styles_part)
            if z_m:
                z_val = int(z_m.group(1))
                if z_val >= 9999:
                    indicators.add(f"z-index={z_val}")

            # 3) height=100% / width=100%
            if re.search(r'height\s*:\s*100%', styles_part):
                indicators.add("height=100%")
            if re.search(r'width\s*:\s*100%', styles_part):
                indicators.add("width=100%")

            # 4) top|bottom|left|right=0
            if re.search(r'(top|bottom|left|right)\s*:\s*0', styles_part):
                indicators.add("covers-edge=0")

            # 5) height: (\d+)px => big header detection
            hpx = re.search(r'height\s*:\s*(\d+)px', styles_part)
            if hpx:
                indicators.add(f"heightPX={hpx.group(1)}")

            if not indicators:
                continue

            raw_selectors = selectors_part.split(",")
            for sel in raw_selectors:
                sel = sel.strip()
                if sel not in css_findings:
                    css_findings[sel] = set()
                css_findings[sel].update(indicators)

    return css_findings

def match_selectors_to_elements(soup, css_findings):
    """
    Empareja cada selector (p.ej. ".sticky-header") con elementos reales del DOM.
    Soporta:
      - .clase
      - #id
      - nombre de tag (simplificado)
    """
    matched = {}
    for selector, indicators in css_findings.items():
        if selector.startswith("."):
            cls_name = selector[1:]
            found = soup.find_all(class_=cls_name)
        elif selector.startswith("#"):
            id_name = selector[1:]
            fe = soup.find(id=id_name)
            found = [fe] if fe else []
        else:
            found = soup.find_all(selector)

        for el in found:
            if not el:
                continue
            if el not in matched:
                matched[el] = set()
            matched[el].update(indicators)

    return matched

def run_all___2_4_11(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    # Preparamos las líneas para snippet
    lines = html_content.splitlines()

    # 1) Parse <style> y extrae indicadores
    css_findings = parse_style_blocks_for_selectors(soup)

    # 2) Emparejar con elementos del DOM
    matched_selectors = match_selectors_to_elements(soup, css_findings)

    # 3) Revisar inline style => fallback
    for el in soup.find_all(style=True):
        st = el["style"].lower()
        indicators = set()

        if re.search(r'position\s*:\s*(fixed|sticky)', st):
            p = re.search(r'position\s*:\s*(fixed|sticky)', st)
            indicators.add(f"position={p.group(1)}")

        z_m = re.search(r'z-index\s*:\s*(\d+)', st)
        if z_m:
            zv = int(z_m.group(1))
            if zv >= 9999:
                indicators.add(f"z-index={zv}")

        if re.search(r'height\s*:\s*100%', st):
            indicators.add("height=100%")
        if re.search(r'width\s*:\s*100%', st):
            indicators.add("width=100%")

        if re.search(r'(top|bottom|left|right)\s*:\s*0', st):
            indicators.add("covers-edge=0")

        # height px
        hpx = re.search(r'height\s*:\s*(\d+)px', st)
        if hpx:
            indicators.add(f"heightPX={hpx.group(1)}")

        if indicators:
            if el not in matched_selectors:
                matched_selectors[el] = set()
            matched_selectors[el].update(indicators)

    # 4) Heurísticas finales
    incidences = []
    for el, indicators in matched_selectors.items():
        info = get_element_info(el, html_lines=lines)

        # a) full overlay => height=100% or width=100% + covers-edge=0
        if (("height=100%" in indicators) or ("width=100%" in indicators)) and ("covers-edge=0" in indicators):
            incidences.append({
                "title": "Possible full-page overlay covering focus",
                "type": "Focus Not Obscured",
                "severity": "High",
                "expected_result": (
                    "Focused items remain at least partially visible. A 100% overlay at edges can hide them fully."
                ),
                "actual_result": "An element with full coverage plus top/left=0 found.",
                "remediation": (
                    "Ensure the overlay doesn't obscure focus items. Use partial coverage or scroll-padding. "
                    "Or treat it as a modal if intended."
                ),
                "wcag_reference": "2.4.11",
                "impact": "Keyboard users might not see which item is focused behind this overlay.",
                "page_url": page_url,
                "element_info": info
            })

        # b) z-index >= 9999
        big_z = next((x for x in indicators if x.startswith("z-index=")), None)
        if big_z:
            val = int(big_z.split("=")[1])
            if val >= 9999:
                incidences.append({
                    "title": "Extremely high z-index might fully obscure underlying focus",
                    "type": "Focus Not Obscured",
                    "severity": "Medium",
                    "expected_result": "Focus never fully hidden by top layers.",
                    "actual_result": f"Element has z-index={val}. Potential to hide focus behind it.",
                    "remediation": "Use lower z-index or ensure user can scroll/close/hide the overlay.",
                    "wcag_reference": "2.4.11",
                    "impact": "Keyboard focus behind may be invisible to sighted keyboard users.",
                    "page_url": page_url,
                    "element_info": info
                })

        # c) fixed + large header => position=fixed + top=0 + heightPX>=100
        pos_fixed = any(s == "position=fixed" for s in indicators)
        top0 = ("covers-edge=0" in indicators)  # sign of top or left or bottom or right=0
        height_px = next((x for x in indicators if x.startswith("heightPX=")), None)
        if pos_fixed and top0 and height_px:
            val = int(height_px.split("=")[1])
            if val >= 100:
                incidences.append({
                    "title": "Large fixed header could hide keyboard focus",
                    "type": "Focus Not Obscured",
                    "severity": "Medium",
                    "expected_result": "Focus remains partially visible behind the header.",
                    "actual_result": f"Fixed header height={val}px at top=0 might obscure items behind it.",
                    "remediation": "Use scroll-padding-top or other technique so focus items are partially visible.",
                    "wcag_reference": "2.4.11",
                    "impact": "Keyboard focus could be out of view under the header.",
                    "page_url": page_url,
                    "element_info": info
                })

    if incidences:
        results = [format_incidence(i) for i in incidences]
        transform_json_to_excel(results, excel)
        return results

    print("No potential overlays/fixed headers that obscure focus were found.")
    return []
