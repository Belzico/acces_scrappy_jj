from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    """Devuelve información detallada del elemento HTML para el reporte."""
    tag = element.name
    element_id = element.get("id", "")
    element_name = element.get("name", "")
    element_class = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    evidence_parts = []
    if element_class:
        evidence_parts.append(f"class={element_class}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if element_name:
        evidence_parts.append(f"name={element_name}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")

    evidence_str = ", ".join(evidence_parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_str else tag

    return {
        "tag": tag,
        "id": element_id or "N/A",
        "name": element_name or "N/A",
        "class": element_class or "N/A",
        "line_number": line_number,
        "evidence": evidence,
        "text": element.get_text(strip=True)[:50]
    }

def format_incidence(old):
    """Convierte una incidencia cruda al formato estandarizado para el reporte."""
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Locate the form field: {old.get('element_info', {}).get('tag', 'N/A')}\n"
            f"3. Trigger validation and check if error message is present and visible."
        ),
        "Bug Type": old.get("type"),
        "Priority": old.get("severity"),
        "Expected Result": old.get("expected_result", "N/A"),
        "Actual Result": old.get("actual_result", "N/A"),
        "Suggested resolution(s)": old.get("remediation"),
        "Failed checkpoint": old.get("wcag_reference"),
        "User Impact": old.get("impact"),
        "Evidence [SS or Video]": old.get("element_info", {}).get("evidence", "N/A")
    }

def check_form_error_identification(html_content, page_url):
    """
    Verifica que los campos de formulario con errores muestren mensajes visibles.
    Criterio: WCAG 3.3.1 - Error Identification.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    incidences = []

    error_fields = soup.find_all(lambda tag: 
        tag.name in ["input", "textarea", "select"] and 
        tag.has_attr("aria-invalid") and 
        tag["aria-invalid"].lower() == "true"
    )

    for field in error_fields:
        field_name = field.get("name") or field.get("id") or "Unnamed field"
        error_text = None
        element_info = get_element_info(field)

        # 1️⃣ Verificar si hay mensaje de error referenciado con aria-describedby
        described_by = field.get("aria-describedby")
        if described_by:
            described_error = soup.find(id=described_by)
            if described_error and described_error.get_text(strip=True):
                if not described_error.has_attr("style") or "display: none" not in described_error["style"]:
                    error_text = described_error.get_text(strip=True)

        # 2️⃣ Buscar mensaje de error adyacente
        if not error_text:
            next_sibling = field.find_next_sibling()
            while next_sibling:
                if next_sibling.name in ["span", "div", "p", "small"] and "error" in " ".join(next_sibling.get("class", [])):
                    if not next_sibling.has_attr("style") or "display: none" not in next_sibling["style"]:
                        error_text = next_sibling.get_text(strip=True)
                        break
                next_sibling = next_sibling.find_next_sibling()

        # 3️⃣ Si no hay mensaje visible, registrar incidencia
        if not error_text:
            incidences.append({
                "title": "Form field missing visible error message",
                "type": "Error Identification",
                "severity": "High",
                "expected_result": "Each invalid field must have a visible and descriptive error message.",
                "actual_result": f"The field '{field_name}' is marked as invalid but no visible error message was found.",
                "remediation": (
                    "Ensure a visible text error message is placed next to the field or "
                    "linked using aria-describedby."
                ),
                "wcag_reference": "3.3.1",
                "impact": "Users may not understand what error needs correction.",
                "page_url": page_url,
                "element_info": element_info
            })

    return incidences

def run_all___3_3_1(html_content, page_url, excel="issue_report.xlsx"):
    """
    Integrador para WCAG 3.3.1 - Error Identification.
    Ejecuta el checker y genera el Excel de reporte.
    """
    raw = check_form_error_identification(html_content, page_url)
    formatted = [format_incidence(inc) for inc in raw]

    if formatted:
        transform_json_to_excel(formatted, excel)

    return formatted
