import re
from bs4 import BeautifulSoup
from collections import defaultdict
from transform_json_to_excel import transform_json_to_excel

# --- Funciones para extraer líneas de HTML y snippet ---
def get_html_lines(html_content):
    """
    Dado el HTML como string, lo dividimos por líneas.
    Útil para luego extraer un snippet alrededor de la línea donde se encontró un error.
    """
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    lines: lista de líneas del HTML (salida de get_html_lines).
    line_number: número de línea (base 1) donde se encontró el elemento.
    context: cuántas líneas antes y después se extraen.

    Retorna un string con el fragmento de HTML alrededor de esa línea,
    enumerando cada línea real para depuración.
    """
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(
        f"{i+1}: {lines[i]}"
        for i in range(start, end)
    )
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Devuelve información del elemento afectado, y si se proporcionan html_lines,
    extrae un snippet (fragment_html) alrededor de la línea del elemento.
    """
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    # Si fuera <img>, podríamos extraer el nombre del archivo src
    src_snippet = ""
    if tag == "img":
        full_src = element.get("src", "")
        src_snippet = full_src.split("/")[-1] if full_src else ""

    evidence_parts = []
    if classes:
        evidence_parts.append(f"class={classes}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")
    if src_snippet:
        evidence_parts.append(f"src={src_snippet}")

    evidence_str = ", ".join(evidence_parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_str else tag

    # Extraer snippet de HTML alrededor de line_number, si es numérico
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
        "fragment_html": snippet_str  # <-- El snippet contextual se almacena aquí
    }

def format_incidence(old):
    """
    Formatea una incidencia para el reporte Excel con todos los campos requeridos,
    incluyendo la evidencia y el snippet HTML.
    """
    elem_info = old.get("element_info", {})
    snippet = elem_info.get("fragment_html", "")
    line_number = elem_info.get("line_number", "N/A")

    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {elem_info.get('tag', 'N/A')}\n"
            f"3. Check the relevant ARIA attributes.\n\n"
            f"HTML snippet (around line {line_number}):\n"
            f"{snippet}"
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("description"),
        "Actual Result": old.get("impact"),
        "Suggested resolution(s)": old.get("remediation"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact"),
        "Evidence [SS or Video]": elem_info.get("evidence", "N/A")
    }

# --- Individual checkers ---
def check_accordion_aria_expanded(soup, lines, page_url):
    accordion_buttons = soup.find_all("button", class_="accordion-toggle")
    accordion_buttons += soup.find_all(attrs={"role": "button", "class": "accordion-toggle"})
    accordion_buttons += soup.find_all("a", class_="accordion-toggle")
    incidences = []

    for btn in accordion_buttons:
        if btn.get("aria-expanded") not in ["true", "false"]:
            issue = {
                "title": "Accordion items do not announce their state",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    "Accordion buttons must have aria-expanded to announce their state "
                    "to assistive technologies."
                ),
                "impact": (
                    "One or more accordion buttons are missing the `aria-expanded` attribute. "
                    "Screen reader users may not be aware of expandable content."
                ),
                "remediation": "Add `aria-expanded=\"true\"` or `aria-expanded=\"false\"` to the accordion button.",
                "wcag_reference": "4.1.2",
                "page_url": page_url,
                "element_info": get_element_info(btn, html_lines=lines)
            }
            incidences.append(format_incidence(issue))
    return incidences

def check_aria_label_in_div(soup, lines, page_url):
    divs_with_aria_label = soup.find_all("div", attrs={"aria-label": True})
    incidences = []

    for div in divs_with_aria_label:
        if not div.has_attr("role"):
            issue = {
                "title": "ARIA label used in <div> without a role",
                "type": "HTML Validator",
                "severity": "Low",
                "description": (
                    "ARIA labels must be used on elements that support them, "
                    "together with an appropriate role if needed."
                ),
                "impact": (
                    "This <div> uses aria-label but has no role, which can confuse "
                    "validators or assistive technologies."
                ),
                "remediation": "Ensure that <div> elements with `aria-label` have an appropriate `role` if they are interactive.",
                "wcag_reference": "4.1.2",
                "page_url": page_url,
                "element_info": get_element_info(div, html_lines=lines)
            }
            incidences.append(format_incidence(issue))
    return incidences

def check_button_aria_expanded(soup, lines, page_url):
    buttons = soup.find_all("button") + soup.find_all(attrs={"role": "button"}) + soup.find_all(attrs={"aria-expanded": True})
    incidences = []

    for btn in buttons:
        if btn.get("aria-expanded") not in ["true", "false"]:
            issue = {
                "title": "Expandable button missing aria-expanded",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    "Expandable buttons must have `aria-expanded` to reflect their "
                    "current state (collapsed or expanded)."
                ),
                "impact": (
                    "These buttons do not have the `aria-expanded` attribute, so screen "
                    "reader users cannot know if they are expanded or collapsed."
                ),
                "remediation": "Ensure expandable buttons include `aria-expanded`.",
                "wcag_reference": "4.1.2",
                "page_url": page_url,
                "element_info": get_element_info(btn, html_lines=lines)
            }
            incidences.append(format_incidence(issue))
    return incidences

def check_button_aria_pressed(soup, lines, page_url):
    buttons = soup.find_all(attrs={"role": "button"})
    selected_button_found = any(button.get("aria-pressed") == "true" for button in buttons)
    incidences = []

    if not selected_button_found:
        issue = {
            "title": "Selected button state is not announced",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": (
                "Toggle/selected buttons must have `aria-pressed=\"true\"` "
                "to indicate their pressed state."
            ),
            "impact": (
                "No buttons have `aria-pressed=\"true\"`, so the selected/pressed state "
                "is not communicated to screen reader users."
            ),
            "remediation": "Mark the selected button with `aria-pressed=\"true\"`.",
            "wcag_reference": "4.1.2",
            "page_url": page_url,
            "element_info": {
                "tag": "button", "id": "N/A", "class": "N/A",
                "line_number": "N/A", "evidence": "button", "fragment_html": ""
            }
        }
        incidences.append(format_incidence(issue))
    return incidences

def check_combobox_aria_expanded(soup, lines, page_url):
    comboboxes = soup.find_all("input", attrs={"role": "combobox"})
    comboboxes += soup.find_all("div", attrs={"role": "combobox"})
    comboboxes += soup.find_all("select", attrs={"aria-expanded": True})
    incidences = []

    for cb in comboboxes:
        if cb.get("aria-expanded") not in ["true", "false"]:
            issue = {
                "title": "Search combobox missing aria-expanded",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    "Combobox controls must update `aria-expanded` to reflect "
                    "their expanded/collapsed state."
                ),
                "impact": (
                    "This combobox does not have or update `aria-expanded`, so screen "
                    "reader users may be confused."
                ),
                "remediation": "Ensure combobox updates `aria-expanded` when expanded/collapsed.",
                "wcag_reference": "4.1.2",
                "page_url": page_url,
                "element_info": get_element_info(cb, html_lines=lines)
            }
            incidences.append(format_incidence(issue))
    return incidences

def check_mobile_button_aria_expanded(soup, lines, page_url):
    buttons = soup.find_all("button") + soup.find_all(attrs={"role": "button"}) + soup.find_all(attrs={"aria-expanded": True})
    incorrect_buttons = [btn for btn in buttons if btn.get("aria-expanded") not in ["true", "false"]]
    incidences = []

    if incorrect_buttons:
        issue = {
            "title": "Button has no expanded/collapsed state announced on mobile",
            "type": "Screen Readers",
            "severity": "Medium",
            "description": (
                "Expandable buttons on mobile must have `aria-expanded=\"true\"` or "
                "`aria-expanded=\"false\"` so users know their state."
            ),
            "impact": (
                "One or more buttons are missing `aria-expanded`, so screen reader users "
                "on mobile won't get the expand/collapse state."
            ),
            "remediation": "Add `aria-expanded=\"true\"` or `aria-expanded=\"false\"`.",
            "wcag_reference": "4.1.2",
            "page_url": page_url,
            "element_info": get_element_info(incorrect_buttons[0], html_lines=lines)
        }
        incidences.append(format_incidence(issue))
    return incidences

def check_name_role_value(soup, lines, page_url):
    incidences = []
    elements = soup.find_all(["button", "input", "textarea", "select", "a", "div", "span"])

    for el in elements:
        info = get_element_info(el, html_lines=lines)
        has_name = el.get_text(strip=True) or el.get("aria-label") or el.get("aria-labelledby")
        if not has_name:
            incidences.append(format_incidence({
                "title": "Missing accessible name",
                "type": "Name, Role, Value",
                "severity": "High",
                "description": (
                    "Elements must have an accessible name (inner text, aria-label, or aria-labelledby)."
                ),
                "impact": (
                    f"The element '{info['tag']}' with ID '{info['id']}' does not have an "
                    "accessible name, so screen reader users can't identify its purpose."
                ),
                "remediation": (
                    "Add an aria-label, aria-labelledby, or provide textual content."
                ),
                "wcag_reference": "4.1.2",
                "page_url": page_url,
                "element_info": info
            }))

        # Missing accessible role (para div/span interactivos)
        if el.name in ["div", "span"] and not el.get("role"):
            incidences.append(format_incidence({
                "title": "Missing accessible role",
                "type": "Name, Role, Value",
                "severity": "Medium",
                "description": (
                    "Non-semantic elements (div/spans) acting as interactive controls "
                    "need a proper role attribute."
                ),
                "impact": (
                    f"The element '{info['tag']}' with ID '{info['id']}' does not have a defined role, "
                    "so assistive technologies may not interpret it correctly."
                ),
                "remediation": "Add an appropriate 'role' (e.g., role='button').",
                "wcag_reference": "4.1.2",
                "page_url": page_url,
                "element_info": info
            }))

        # Missing programmatic value para checkboxes/radios
        if el.name == "input" and el.get("type") in ["checkbox", "radio"]:
            if "aria-checked" not in el.attrs and "checked" not in el.attrs:
                incidences.append(format_incidence({
                    "title": "Missing programmatic value",
                    "type": "Name, Role, Value",
                    "severity": "High",
                    "description": (
                        "Checkboxes/radios must convey their state (checked or not) with "
                        "`checked` o `aria-checked`."
                    ),
                    "impact": (
                        f"The checkbox/radio '{info['id']}' doesn't have a programmatically determined state, "
                        "so screen reader users won't know if it's selected."
                    ),
                    "remediation": "Add 'aria-checked' or 'checked' to indicate the selected state.",
                    "wcag_reference": "4.1.2",
                    "page_url": page_url,
                    "element_info": info
                }))
    return incidences

def check_tab_aria_selected(soup, lines, page_url):
    tabs = soup.find_all(attrs={"role": "tab"})
    selected_tab_found = any(tab.get("aria-selected") == "true" for tab in tabs)
    incidences = []

    if not selected_tab_found and tabs:
        issue = {
            "title": "Selected tab state is not announced",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": (
                "The active/selected tab must have `aria-selected=\"true\"` so users "
                "know which tab is active."
            ),
            "impact": (
                "None of the tabs have `aria-selected=\"true\"`, so screen reader users "
                "cannot tell which tab is selected."
            ),
            "remediation": "Add `aria-selected=\"true\"` to the active tab.",
            "wcag_reference": "4.1.2",
            "page_url": page_url,
            "element_info": get_element_info(tabs[0], html_lines=lines)  # snippet de la primera tab
        }
        incidences.append(format_incidence(issue))
    elif not selected_tab_found:
        # Caso: No existen tabs
        issue = {
            "title": "No tabs found or no tab has aria-selected",
            "type": "Screen Reader",
            "severity": "Medium",
            "description": (
                "The page should have at least one tab with `aria-selected=\"true\"` to "
                "indicate the active tab."
            ),
            "impact": "Screen reader users cannot identify any tab as selected.",
            "remediation": "Ensure at least one tab is marked with `aria-selected=\"true\"`.",
            "wcag_reference": "4.1.2",
            "page_url": page_url,
            "element_info": {
                "tag": "tab",
                "id": "N/A",
                "class": "N/A",
                "line_number": "N/A",
                "evidence": "tab",
                "fragment_html": ""
            }
        }
        incidences.append(format_incidence(issue))

    return incidences

# --- Integrador principal ---
def run_all___4_1_2(html_content, page_url, excel="issue_report.xlsx"):
    """
    Ejecuta todos los checkers para 4.1.2, generando incidencias con snippet de HTML
    donde corresponde. Si hay incidencias, las exporta a Excel.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)  # Separa el HTML por líneas para extraer snippets

    all_issues = []
    all_issues += check_accordion_aria_expanded(soup, lines, page_url)
    all_issues += check_aria_label_in_div(soup, lines, page_url)
    all_issues += check_button_aria_expanded(soup, lines, page_url)
    all_issues += check_button_aria_pressed(soup, lines, page_url)
    all_issues += check_combobox_aria_expanded(soup, lines, page_url)
    all_issues += check_mobile_button_aria_expanded(soup, lines, page_url)
    all_issues += check_name_role_value(soup, lines, page_url)
    all_issues += check_tab_aria_selected(soup, lines, page_url)

    if all_issues:
        transform_json_to_excel(all_issues, excel)

    return all_issues
