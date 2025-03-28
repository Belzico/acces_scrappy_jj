from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel
from sentence_transformers import SentenceTransformer, util

# Cargar modelo de embeddings para comparación semántica
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def get_element_info(element):
    """
    Devuelve información del elemento afectado y genera una evidencia única y buscable.
    Ejemplo de evidencia: img[class=logo, id=main-logo, line=45, src=logo.png]
    """
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    # Extraer el nombre del archivo del atributo src si existe (para <img>)
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
    evidence = f"{tag}[{evidence_str}]"

    return {
        "tag": tag,
        "text": element.get_text(strip=True)[:50],
        "id": element_id or "N/A",
        "class": classes or "N/A",
        "line_number": line_number,
        "evidence": evidence
    }


def format_incidence(old):
    """Formatea una incidencia para el reporte Excel con todos los campos requeridos."""
    return {
        "Title": old.get("title"),
        "Steps": (
            f"1. Open the page: {old.get('page_url')}\n"
            f"2. Inspect the element: {old.get('element_info', {}).get('tag', 'N/A')}\n"
            f"3. Review the ARIA or ALT attributes and surrounding context."
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

# 1️⃣ check_alt_distinction
def check_alt_distinction(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    incidences = []
    images = soup.find_all("img")

    for img in images:
        alt = img.get("alt", None)
        parent = img.parent
        info = get_element_info(img)

        if alt is None:
            incidences.append(format_incidence({
                "title": "Image missing alt attribute",
                "type": "Alternative Text",
                "severity": "High",
                "description": "All images must have an alt attribute (descriptive or empty if purely decorative).",
                "impact": "This image does not have an alt attribute. Screen reader users may not understand its purpose.",
                "remediation": "Add an appropriate alt attribute.",
                "wcag_reference": "1.1.1",
                "page_url": page_url,
                "element_info": info
            }))
            continue

        if alt.strip() == "" and parent and parent.name in ["a", "button"]:
            link_text = "".join(parent.stripped_strings)
            aria_label = parent.get("aria-label", "")
            if not link_text and not aria_label:
                incidences.append(format_incidence({
                    "title": "Link/Button with no accessible text",
                    "type": "Alternative Text",
                    "severity": "High",
                    "description": "Links/Buttons must have accessible text or aria-label to describe their function.",
                    "impact": "The image inside the link/button has alt='', and there is no link text or aria-label. Screen readers won't know its purpose.",
                    "remediation": "Add accessible text or aria-label.",
                    "wcag_reference": "1.1.1",
                    "page_url": page_url,
                    "element_info": get_element_info(parent)
                }))
            continue

        # Comprobación de redundancia semántica
        alt_text = alt.strip()
        previous_text = img.find_previous(string=True, recursive=True)
        next_text = img.find_next(string=True, recursive=True)
        previous_text = previous_text.strip() if previous_text else ""
        next_text = next_text.strip() if next_text else ""
        adjacent_text = f"{previous_text} {next_text}".strip()

        if adjacent_text:
            alt_embedding = model.encode(alt_text, convert_to_tensor=True)
            adj_embedding = model.encode(adjacent_text, convert_to_tensor=True)
            similarity = util.cos_sim(alt_embedding, adj_embedding).item()
            if similarity > 0.8:
                incidences.append(format_incidence({
                    "title": "Redundant alternative text (semantic match)",
                    "type": "Alternative Text",
                    "severity": "Medium",
                    "description": "The alt text should not duplicate adjacent text. It must be unique or empty if purely decorative.",
                    "impact": f"The alt text is semantically similar to nearby text (similarity={similarity:.2f}), causing redundant information.",
                    "remediation": "Use alt='' if decorative, or ensure alt is sufficiently unique.",
                    "wcag_reference": "1.1.1",
                    "page_url": page_url,
                    "element_info": info
                }))

    return incidences


# 2️⃣ check_icons_informative
def check_icons_informative(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    incidences = []

    for icon in soup.find_all(["span", "i"], class_=["icon", "fa", "material-icons"]):
        aria_hidden = icon.get("aria-hidden")
        has_text = bool(icon.text.strip())
        info = get_element_info(icon)

        if aria_hidden is None or aria_hidden.lower() != "true":
            if not has_text:
                incidences.append(format_incidence({
                    "title": "Informative icon is not announced",
                    "type": "Screen Reader",
                    "severity": "High",
                    "description": "Icons that convey meaning must have an accessible label (e.g., aria-label) or visible text.",
                    "impact": "This icon provides meaning but does not have an accessible label or aria-hidden. Screen readers won't announce it.",
                    "remediation": "Use aria-label or provide visually hidden text.",
                    "wcag_reference": "1.1.1",
                    "page_url": page_url,
                    "element_info": info
                }))

    return incidences


# 3️⃣ check_images_decorative
def check_images_decorative(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    incidences = []

    for img in soup.find_all("img"):
        alt = img.get("alt")
        if alt is None:
            incidences.append(format_incidence({
                "title": "Missing alt attribute",
                "type": "Screen Reader",
                "severity": "High",
                "description": "Decorative images should have alt='' or a role='presentation'. Informative ones require descriptive alt.",
                "impact": "This image is missing an alt attribute, which can confuse screen reader users (they may hear a filename).",
                "remediation": "Use alt='' for decorative images or provide descriptive alt if informative.",
                "wcag_reference": "1.1.1",
                "page_url": page_url,
                "element_info": get_element_info(img)
            }))

    return incidences


# 4️⃣ check_informative_images
def check_informative_images(html_content, page_url):
    soup = BeautifulSoup(html_content, "html.parser")
    incidences = []

    for img in soup.find_all("img"):
        alt = img.get("alt")
        if alt is None or alt.strip() == "":
            incidences.append(format_incidence({
                "title": "Informative image with missing or empty alt",
                "type": "Screen Reader",
                "severity": "High",
                "description": "Informative images must include a concise alt text describing their content or function.",
                "impact": "This image is missing an alt text (or it's empty), so users miss the information conveyed by the image.",
                "remediation": "Add a short descriptive alt text.",
                "wcag_reference": "1.1.1",
                "page_url": page_url,
                "element_info": get_element_info(img)
            }))

    return incidences


# 🚀 Integrador principal
def run_all___1_1_1(html_content, page_url, excel="issue_report.xlsx"):
    all_issues = []
    all_issues += check_alt_distinction(html_content, page_url)
    all_issues += check_icons_informative(html_content, page_url)
    all_issues += check_images_decorative(html_content, page_url)
    all_issues += check_informative_images(html_content, page_url)

    if all_issues:
        transform_json_to_excel(all_issues, excel)

    return all_issues
