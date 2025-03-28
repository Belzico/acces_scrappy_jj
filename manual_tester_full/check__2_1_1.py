from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel


def get_element_info(element):
    """Devuelve información detallada del elemento HTML con evidencia rastreable."""
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

    evidence = f"{tag}[{', '.join(evidence_parts)}]" if evidence_parts else tag

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }


def format_incidence(inc):
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the element: {inc.get('element_info', {}).get('tag', 'N/A')}\n"
            f"3. Review its event attributes and keyboard support."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result", "N/A"),
        "Actual Result": inc.get("actual_result", "N/A"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact", "N/A"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "N/A")
    }


def run_all___2_1_1(html_content, page_url, excel="issue_report.xlsx"):
    """
    Ejecuta el checker de accesibilidad por teclado para WCAG 2.1.1.
    Incluye detección de eventos de mouse sin soporte equivalente de teclado.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 1️⃣ Elementos con eventos de mouse sin equivalentes de teclado
    elements_with_mouse_events = soup.find_all(onclick=True) + \
                                 soup.find_all(onmouseover=True) + \
                                 soup.find_all(onmouseenter=True)

    for element in elements_with_mouse_events:
        info = get_element_info(element)
        missing_keyboard_support = []

        if "onkeydown" not in element.attrs and "onkeypress" not in element.attrs:
            missing_keyboard_support.append("onkeydown")

        if "onfocus" not in element.attrs and ("onmouseover" in element.attrs or "onmouseenter" in element.attrs):
            missing_keyboard_support.append("onfocus")

        if element.name in ["span", "div"] and "onclick" in element.attrs and "tabindex" not in element.attrs:
            missing_keyboard_support.append("tabindex='0'")

        if missing_keyboard_support:
            raw_incidences.append({
                "title": "Element with mouse events but no keyboard support",
                "type": "Keyboard Accessibility",
                "severity": "High",
                "expected_result": f"Interactive elements must respond to keyboard inputs such as {', '.join(missing_keyboard_support)}.",
                "actual_result": f"The element uses {', '.join(element.attrs.keys())} but lacks keyboard equivalents: {', '.join(missing_keyboard_support)}.",
                "remediation": f"Add handlers for {', '.join(missing_keyboard_support)} to make it keyboard accessible.",
                "wcag_reference": "2.1.1",
                "impact": "Users who rely on keyboard cannot interact with this element.",
                "page_url": page_url,
                "element_info": info
            })

    # 2️⃣ Revisar scripts con eventos mal implementados
    script_tags = soup.find_all("script")
    js_patterns = {
        "click_no_keydown": re.compile(r'\.addEventListener\s*\(\s*[\'"]click[\'"]'),
        "mouseover_no_focus": re.compile(r'\.addEventListener\s*\(\s*[\'"]mouseover[\'"]'),
        "mouseenter_no_focus": re.compile(r'\.addEventListener\s*\(\s*[\'"]mouseenter[\'"]'),
        "hidden_no_aria": re.compile(r'\.style\.display\s*=\s*[\'"]none[\'"]')
    }

    for script in script_tags:
        script_content = script.string
        if not script_content:
            continue

        info = get_element_info(script)

        if js_patterns["click_no_keydown"].search(script_content) and "keydown" not in script_content:
            raw_incidences.append({
                "title": "Click handler in JS without keydown equivalent",
                "type": "Keyboard Accessibility",
                "severity": "High",
                "expected_result": "Keyboard equivalents (e.g. keydown) should be added when using click in JS.",
                "actual_result": "addEventListener('click') is used without any keydown handler.",
                "remediation": "Add addEventListener('keydown', ...) to support keyboard users.",
                "wcag_reference": "2.1.1",
                "impact": "Users without a mouse can't trigger the interaction.",
                "page_url": page_url,
                "element_info": info
            })

        if js_patterns["mouseover_no_focus"].search(script_content) and "focus" not in script_content:
            raw_incidences.append({
                "title": "Mouseover handler without focus",
                "type": "Keyboard Accessibility",
                "severity": "Medium",
                "expected_result": "mouseover interactions should have a focus equivalent for keyboard users.",
                "actual_result": "mouseover handler detected but no corresponding focus handler in JS.",
                "remediation": "Add a focus handler alongside mouseover.",
                "wcag_reference": "2.1.1",
                "impact": "Content won't be accessible for keyboard-only users.",
                "page_url": page_url,
                "element_info": info
            })

        if js_patterns["mouseenter_no_focus"].search(script_content) and "focus" not in script_content:
            raw_incidences.append({
                "title": "Mouseenter handler without focus",
                "type": "Keyboard Accessibility",
                "severity": "Medium",
                "expected_result": "mouseenter handlers should be paired with focus handlers for keyboard users.",
                "actual_result": "mouseenter event is used without any focus support.",
                "remediation": "Add a focus handler to make the behavior accessible.",
                "wcag_reference": "2.1.1",
                "impact": "Keyboard users can't access this feature.",
                "page_url": page_url,
                "element_info": info
            })

        if js_patterns["hidden_no_aria"].search(script_content) and "aria-hidden" not in script_content:
            raw_incidences.append({
                "title": "Content hidden without aria-hidden",
                "type": "Keyboard Accessibility",
                "severity": "Low",
                "expected_result": "When hiding content via display:none, aria-hidden should be added.",
                "actual_result": "Element is hidden via JS but aria-hidden is missing.",
                "remediation": "Call setAttribute('aria-hidden', 'true') when hiding elements.",
                "wcag_reference": "2.1.1",
                "impact": "Assistive technologies may still read hidden content.",
                "page_url": page_url,
                "element_info": info
            })

    # 3️⃣ data-event="mouseover" sin onfocus
    for element in soup.find_all(attrs={"data-event": "mouseover"}):
        info = get_element_info(element)
        if "onfocus" not in element.attrs:
            raw_incidences.append({
                "title": "Element using data-event='mouseover' without onfocus",
                "type": "Keyboard Accessibility",
                "severity": "Medium",
                "expected_result": "All mouseover-triggered elements should be accessible via focus (keyboard).",
                "actual_result": "This element uses data-event='mouseover' but lacks onfocus handler.",
                "remediation": "Add onfocus to trigger the same behavior as mouseover.",
                "wcag_reference": "2.1.1",
                "impact": "Keyboard users cannot trigger the interaction.",
                "page_url": page_url,
                "element_info": info
            })

    formatted = [format_incidence(inc) for inc in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)
    return formatted
