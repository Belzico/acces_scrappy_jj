from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    """
    Devuelve información detallada de un elemento HTML para el reporte.
    """
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    evidence_parts = []
    if classes:
        evidence_parts.append(f"class={classes}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")

    evidence_str = ", ".join(evidence_parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_str else tag

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }

def format_incidence(inc):
    """
    Estructura estandarizada para reportar incidencias.
    """
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the element: {inc.get('element_info', {}).get('tag', 'N/A')}.\n"
            f"3. Verify if the user can tab away using only keyboard."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result", "N/A"),
        "Actual Result": inc.get("actual_result", "N/A"),
        "Suggested resolution(s)": inc.get("remediation", "N/A"),
        "Failed checkpoint": inc.get("wcag_reference", "2.1.2"),
        "User Impact": inc.get("impact", "N/A"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "N/A")
    }

def run_all___2_1_2(html_content, page_url, excel="issue_report.xlsx"):
    """
    Verifica patrones comunes que podrían indicar un atrapamiento de teclado.
      1) Contenedores modales sin botón o sin instructions para salir
      2) Elementos con tabindex > 0 repetidos
      3) Bloques con onkeydown u onkeypress que puedan capturar tab sin onkeyup
      4) Pistas de un "dialog" (role="dialog", aria-modal="true") sin un control para cerrar/escapar
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 1️⃣ Revisar contenedores con role="dialog" o aria-modal="true" (posible modal)
    #    que NO tengan un botón/cerrar
    dialogs = soup.find_all(lambda el:
        (el.has_attr("role") and el["role"] in ["dialog", "alertdialog"]) or
        (el.has_attr("aria-modal") and el["aria-modal"].lower() == "true"))
    for dlg in dialogs:
        # No hay un botón "close" ni "x" ni aria-label ~ "close" => posible trampa
        close_btn = dlg.find(lambda x:
            x.name in ["button", "a"] and
            (
                "close" in (x.get("class") or []) or
                "x" in x.get_text(strip=True).lower() or
                "close" in (x.get("aria-label") or "").lower()
            )
        )
        if not close_btn:
            info = get_element_info(dlg)
            raw_incidences.append({
                "title": "Dialog or modal without an apparent close mechanism",
                "type": "No Keyboard Trap",
                "severity": "High",
                "expected_result": "Focus inside dialogs should be escapable by pressing a close control or ESC.",
                "actual_result": "Found a dialog-like container with no obvious close button/link.",
                "remediation": "Provide a keyboard-accessible way to exit the dialog, e.g. a close button.",
                "wcag_reference": "2.1.2",
                "impact": "Keyboard users might get stuck inside this modal.",
                "page_url": page_url,
                "element_info": info
            })

    # 2️⃣ Revisar tabindex > 0 repetidos, que pueden crear orden de tab complejo o cíclico
    elements_with_tabindex = soup.find_all(lambda el: el.has_attr("tabindex"))
    tabindex_map = {}
    for el in elements_with_tabindex:
        tb = el["tabindex"]
        if tb.isdigit():
            tb_val = int(tb)
            if tb_val > 0:
                tabindex_map.setdefault(tb_val, []).append(el)

    for tb_val, els in tabindex_map.items():
        if len(els) > 2:  # muchos con tabindex>0 => posible caos
            info = get_element_info(els[0])
            raw_incidences.append({
                "title": f"Multiple elements with tabindex={tb_val} (potential trap or unusual order)",
                "type": "No Keyboard Trap",
                "severity": "Medium",
                "expected_result": "Natural tab order or minimal use of positive tabindex.",
                "actual_result": f"Found {len(els)} elements with tabindex={tb_val}. This might cause focus loops.",
                "remediation": "Use tabindex=0 or rely on DOM order instead of positive values.",
                "wcag_reference": "2.1.2",
                "impact": "Keyboard users may navigate in unexpected loops or get stuck.",
                "page_url": page_url,
                "element_info": info
            })

    # 3️⃣ Revisar scripts inline (ej: onkeydown) que capturen TAB sin dejar salir
    #    Ej: 'event.preventDefault()' con keyCode=9. Es un heurístico.
    script_attrs = ["onkeydown", "onkeypress"]
    for el in soup.find_all(lambda x: any(a in x.attrs for a in script_attrs)):
        for attr in script_attrs:
            if attr in el.attrs:
                code = el.attrs[attr].lower()
                # Heurística: si menciona keyCode=9 || event.key=== 'Tab', y hace preventDefault
                if ("keycode" in code and "9" in code and "preventdefault" in code) or \
                   ("tab" in code and "preventdefault" in code):
                    info = get_element_info(el)
                    raw_incidences.append({
                        "title": "Element may trap Tab key",
                        "type": "No Keyboard Trap",
                        "severity": "High",
                        "expected_result": "Allow tab key to move focus away or offer an alternative escape key.",
                        "actual_result": f"'{attr}' handler possibly capturing Tab key (preventDefault).",
                        "remediation": "Ensure a method to move focus away or a documented key to exit.",
                        "wcag_reference": "2.1.2",
                        "impact": "Keyboard users might not navigate beyond this element.",
                        "page_url": page_url,
                        "element_info": info
                    })

    # 4️⃣ Revisar si un dialog anidado no ofrece info. Podríamos buscar si dentro del dialog hay un mention de 'Esc' key
    #    Esto es un plus, no estricto. 
    #    Se omitirá por simplicidad, pero si lo deseas, se puede parsear el texto dentro.

    formatted = [format_incidence(i) for i in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)

    return formatted
