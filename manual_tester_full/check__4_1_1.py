from bs4 import BeautifulSoup
from collections import defaultdict
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    """Recupera información útil del elemento HTML, incluyendo evidencia rastreable."""
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
    Transforma una incidencia al formato estandarizado de Excel.
    """
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {old.get('element_info', {}).get('tag', 'N/A')}\n"
            "3. Check the relevant ARIA attributes or HTML structure."
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("expected_result", old.get("description")),
        "Actual Result": old.get("actual_result", old.get("impact")),
        "Suggested resolution(s)": old.get("remediation"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact"),
        "Evidence [SS or Video]": old.get("element_info", {}).get("evidence", "N/A")
    }

def run_all___4_1_1(html_content, page_url, excel="issue_report.xlsx"):
    """
    Evalúa el cumplimiento del criterio WCAG 4.1.1: Uso correcto de IDs y estructura semántica en listas.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 🔁 Check 1: Duplicate IDs
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
            "element_info": get_element_info(elements[0])
        })

    # 🔁 Check 2: <div> directly inside <ul> or <ol>
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
                    "element_info": get_element_info(child)
                })

    formatted_incidences = [format_incidence(inc) for inc in raw_incidences]
    if formatted_incidences:
        transform_json_to_excel(formatted_incidences, excel)
    return formatted_incidences
