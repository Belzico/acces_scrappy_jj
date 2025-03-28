from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    """
    Devuelve información del elemento afectado y genera una evidencia única y buscable.
    Ejemplo de evidencia: button[class=accordion-toggle, id=panel1, line=45]
    """
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    # Si fuera un <img>, podríamos extraer el nombre del archivo src, pero aquí no es estrictamente necesario:
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

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }


def format_incidence(old):
    """
    Formatea una incidencia para el reporte Excel con todos los campos requeridos,
    incluyendo evidencia (tag, clase, id, línea) donde se encontró el problema.
    """
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {old.get('element_info', {}).get('tag', 'N/A')}\n"
            f"3. Check the relevant ARIA attributes."
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("description"),
        "Actual Result": old.get("impact"),
        "Suggested resolution(s)": old.get("remediation"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact"),
        "Evidence [SS or Video]": old.get("element_info", {}).get("evidence", "N/A")
    }


# --- Individual checkers ---

def check_accordion_aria_expanded(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    accordion_buttons = soup.find_all("button", class_="accordion-toggle")
    accordion_buttons += soup.find_all(attrs={"role": "button", "class": "accordion-toggle"})
    accordion_buttons += soup.find_all("a", class_="accordion-toggle")
    incidences = []

    for btn in accordion_buttons:
        # Verifica si aria-expanded no está definido como "true" o "false"
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
                "element_info": get_element_info(btn)
            }
            incidences.append(format_incidence(issue))
    return incidences


def check_aria_label_in_div(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    divs_with_aria_label = soup.find_all("div", attrs={"aria-label": True})
    incidences = []

    for div in divs_with_aria_label:
        # Si un div usa aria-label pero no tiene un rol, podría ser un error
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
                "element_info": get_element_info(div)
            }
            incidences.append(format_incidence(issue))
    return incidences


def check_button_aria_expanded(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    # Selecciona <button>, o elementos con role="button", o que tengan aria-expanded
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
                "element_info": get_element_info(btn)
            }
            incidences.append(format_incidence(issue))
    return incidences


def check_button_aria_pressed(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    buttons = soup.find_all(attrs={"role": "button"})
    # Busca si alguno está marcado con aria-pressed="true"
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
            # Element info genérico si no tenemos un botón puntual
            "element_info": {"tag": "button", "id": "N/A", "class": "N/A", "line_number": "N/A", "evidence": "button"}
        }
        incidences.append(format_incidence(issue))
    return incidences


def check_combobox_aria_expanded(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
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
                "element_info": get_element_info(cb)
            }
            incidences.append(format_incidence(issue))
    return incidences


def check_mobile_button_aria_expanded(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
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
            "element_info": get_element_info(incorrect_buttons[0])
        }
        incidences.append(format_incidence(issue))
    return incidences


def check_name_role_value(html_content, page_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    incidences = []
    # Revisamos elementos típicos interactivos + div/span
    elements = soup.find_all(["button", "input", "textarea", "select", "a", "div", "span"])

    for el in elements:
        info = get_element_info(el)
        # 1. Missing accessible name
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

        # 2. Missing accessible role (para div/span interactivos)
        if el.name in ["div", "span"] and not el.get("role"):
            # Podríamos chequear si el div/spa tiene onClick o algo similar para saber si es interactivo
            # pero asumimos que si no tiene role, es un problema potencial.
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

        # 3. Missing programmatic value for checkboxes/radios
        if el.name == "input" and el.get("type") in ["checkbox", "radio"]:
            if "aria-checked" not in el.attrs and "checked" not in el.attrs:
                incidences.append(format_incidence({
                    "title": "Missing programmatic value",
                    "type": "Name, Role, Value",
                    "severity": "High",
                    "description": (
                        "Checkboxes/radios must convey their state (checked or not) with "
                        "`checked` or `aria-checked`."
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


def check_tab_aria_selected(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
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
            "element_info": get_element_info(tabs[0])
        }
        incidences.append(format_incidence(issue))
    elif not selected_tab_found:
        # Caso: No existen tabs o no se pudo identificar ninguno
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
            "element_info": {"tag": "tab", "id": "N/A", "class": "N/A", "line_number": "N/A", "evidence": "tab"}
        }
        incidences.append(format_incidence(issue))

    return incidences


# --- General runner ---
def run_all___4_1_2(html_content, page_url, excel="issue_report.xlsx"):
    all_issues = []
    all_issues += check_accordion_aria_expanded(html_content, page_url)
    all_issues += check_aria_label_in_div(html_content, page_url)
    all_issues += check_button_aria_expanded(html_content, page_url)
    all_issues += check_button_aria_pressed(html_content, page_url)
    all_issues += check_combobox_aria_expanded(html_content, page_url)
    all_issues += check_mobile_button_aria_expanded(html_content, page_url)
    all_issues += check_name_role_value(html_content, page_url)
    all_issues += check_tab_aria_selected(html_content, page_url)

    if all_issues:
        transform_json_to_excel(all_issues, excel)

    return all_issues
