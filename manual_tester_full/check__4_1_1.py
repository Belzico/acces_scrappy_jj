import re
from bs4 import BeautifulSoup
from collections import defaultdict
from transform_json_to_excel import transform_json_to_excel

def get_html_lines(html_content):
    """Convierte el contenido HTML en una lista de líneas para extraer fragmentos contextualizados."""
    return html_content.splitlines()

def get_line_snippet(lines, line_number, context=2):
    """
    Extrae un snippet con 'context' líneas antes y después de line_number (base 1).
    Devuelve un string con numeración para cada línea, facilitando la depuración.
    """
    idx = line_number - 1
    start = max(idx - context, 0)
    end = min(idx + context + 1, len(lines))
    snippet = lines[start:end]
    snippet_str = "\n".join(f"{i+1}: {lines[i]}" for i in range(start, end))
    return snippet_str

def get_element_info(element, html_lines=None):
    """
    Recupera información útil del elemento HTML para el reporte y extrae
    un snippet HTML alrededor de la línea line_number (si existe).
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

    # Extraer snippet contextual (2 líneas antes y después de line_number)
    fragment_html = ""
    if line_number != "N/A" and html_lines:
        try:
            snippet_str = get_line_snippet(html_lines, int(line_number), context=2)
        except ValueError:
            snippet_str = ""
        fragment_html = snippet_str

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence,
        "fragment_html": fragment_html
    }

def format_incidence(old):
    """
    Transforma una incidencia al formato estandarizado de Excel,
    incluyendo un snippet HTML contextual.
    """
    element_info = old.get("element_info", {})
    snippet_context = element_info.get("fragment_html", "")

    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {element_info.get('tag', 'N/A')}\n"
            "3. Check the relevant ARIA attributes or HTML structure.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n"
            f"{snippet_context}"
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("expected_result", old.get("description")),
        "Actual Result": old.get("actual_result", old.get("impact")),
        "Suggested resolution(s)": old.get("remediation"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact"),
        "Evidence [SS or Video]": element_info.get("evidence", "N/A")
    }

def run_all___4_1_1(html_content, page_url, excel="issue_report.xlsx"):
    """
    Evalúa el cumplimiento del criterio WCAG 4.1.1: Uso correcto de IDs y estructura semántica en listas.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    raw_incidences = []

    # 🔁 Check 1: Duplicate IDs
    from collections import defaultdict
    id_elements = defaultdict(list)
    for element in soup.find_all(attrs={"id": True}):
        element_id = element["id"]
        id_elements[element_id].append(element)

    duplicated_ids = {id_: elements for id_, elements in id_elements.items() if len(elements) > 1}

    for id_, elements in duplicated_ids.items():
        raw_incidences.append({
            "title": "Duplicated id in fields",
            "type": "HTML Validator",
            "severity": "High",
            "description": (
                f"The id '{id_}' is used multiple times in {len(elements)} elements."
            ),
            "expected_result": f"The id '{id_}' should appear only once in the HTML document.",
            "actual_result": f"The id '{id_}' is used {len(elements)} times.",
            "remediation": "Ensure all id attributes are unique. Use classes or suffixes to differentiate elements.",
            "wcag_reference": "4.1.1",
            "impact": "Assistive technologies may not correctly associate labels, descriptions, or links.",
            "page_url": page_url,
            "element_info": get_element_info(elements[0], html_lines=lines)
        })

    # 🔁 Check 2: <div> directamente dentro de <ul> o <ol>
    list_elements = soup.find_all(["ul", "ol"])
    for lst in list_elements:
        for child in lst.find_all(recursive=False):
            if child.name == "div":
                raw_incidences.append({
                    "title": "Div elements nested inside ul/ol in the navigation menu",
                    "type": "HTML Validator",
                    "severity": "Low",
                    "description": "A <ul> or <ol> element should not contain <div> elements as direct children.",
                    "expected_result": "<ul> and <ol> should only contain <li>, <script>, or <template> as direct children.",
                    "actual_result": "<div> element found as a direct child of a <ul> or <ol>.",
                    "remediation": "Wrap <div> elements inside a <li> tag. Example: <li><div>Item</div></li>.",
                    "wcag_reference": "4.1.1",
                    "impact": "May affect semantic interpretation and structure by assistive tech.",
                    "page_url": page_url,
                    "element_info": get_element_info(child, html_lines=lines)
                })

    formatted_incidences = [format_incidence(inc) for inc in raw_incidences]
    if formatted_incidences:
        transform_json_to_excel(formatted_incidences, excel)
    return formatted_incidences
