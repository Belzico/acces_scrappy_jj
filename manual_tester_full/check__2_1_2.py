from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel


def get_html_lines(html_content):
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    return "\n".join(f"{i+1}: {snippet[i - start]}" for i in range(start, end))


def get_element_info(element, html_lines=None):
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

    snippet_str = ""
    if line_number != "N/A" and html_lines:
        try:
            snippet_str = get_line_snippet(html_lines, int(line_number))
        except ValueError:
            pass

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence,
        "fragment_html": snippet_str
    }


def format_incidence(inc):
    element_info = inc.get("element_info", {})
    snippet = element_info.get("fragment_html", "")
    return {
        "Title": inc.get("title"),
        "Steps": (
            f"1. Open the page: {inc.get('page_url')}\n"
            f"2. Inspect the element: {element_info.get('tag', 'N/A')}.\n"
            f"3. Verify if the user can tab away using only keyboard.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n"
            f"{snippet}"
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result", "N/A"),
        "Actual Result": inc.get("actual_result", "N/A"),
        "Suggested resolution(s)": inc.get("remediation", "N/A"),
        "Failed checkpoint": inc.get("wcag_reference", "2.1.2"),
        "User Impact": inc.get("impact", "N/A"),
        "Evidence [SS or Video]": element_info.get("evidence", "N/A")
    }


def run_all___2_1_2(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    # 1️⃣ Role="dialog" o aria-modal sin botón de cierre
    dialogs = soup.find_all(lambda el:
        (el.has_attr("role") and el["role"] in ["dialog", "alertdialog"]) or
        (el.has_attr("aria-modal") and el["aria-modal"].lower() == "true"))
    for dlg in dialogs:
        close_btn = dlg.find(lambda x:
            x.name in ["button", "a"] and
            (
                "close" in (x.get("class") or []) or
                "x" in x.get_text(strip=True).lower() or
                "close" in (x.get("aria-label") or "").lower()
            )
        )
        if not close_btn:
            info = get_element_info(dlg, html_lines=lines)
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

    # 2️⃣ tabindex > 0 repetidos
    elements_with_tabindex = soup.find_all(lambda el: el.has_attr("tabindex"))
    tabindex_map = {}
    for el in elements_with_tabindex:
        tb = el["tabindex"]
        if tb.isdigit():
            tb_val = int(tb)
            if tb_val > 0:
                tabindex_map.setdefault(tb_val, []).append(el)

    for tb_val, els in tabindex_map.items():
        if len(els) > 2:
            info = get_element_info(els[0], html_lines=lines)
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

    # 3️⃣ Script inline atrapando Tab
    script_attrs = ["onkeydown", "onkeypress"]
    for el in soup.find_all(lambda x: any(a in x.attrs for a in script_attrs)):
        for attr in script_attrs:
            if attr in el.attrs:
                code = el.attrs[attr].lower()
                if ("keycode" in code and "9" in code and "preventdefault" in code) or \
                   ("tab" in code and "preventdefault" in code):
                    info = get_element_info(el, html_lines=lines)
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

    formatted = [format_incidence(i) for i in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)

    return formatted
