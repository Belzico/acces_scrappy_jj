from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel

def get_element_info(element):
    tag = element.name
    element_id = element.get("id", "")
    classes = " ".join(element.get("class", [])) if element.has_attr("class") else ""
    line_number = element.sourceline if hasattr(element, "sourceline") else "N/A"

    evidence = f"{tag}[id={element_id}, class={classes}, line={line_number}]"
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
            f"2. Inspect the element: {inc.get('element_info', {}).get('tag', 'N/A')}.\n"
            f"3. Confirm it uses semantic HTML for structure and relationships."
        ),
        "Bug Type": inc.get("type"),
        "Priority": inc.get("severity"),
        "Expected Result": inc.get("expected_result"),
        "Actual Result": inc.get("actual_result"),
        "Suggested resolution(s)": inc.get("remediation"),
        "Failed checkpoint": inc.get("wcag_reference"),
        "User Impact": inc.get("impact"),
        "Evidence [SS or Video]": inc.get("element_info", {}).get("evidence", "N/A")
    }

def run_all___1_3_1(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    raw_incidences = []

    # 1️⃣ Detect <b>, <i>, <u> instead of semantic tags
    for tag in soup.find_all(["b", "i", "u"]):
        raw_incidences.append({
            "title": "Non-semantic tag used for styling",
            "type": "Semantic Structure",
            "severity": "Medium",
            "expected_result": "Use semantic elements like <strong>, <em> or CSS for emphasis.",
            "actual_result": f"Element <{tag.name}> used, which conveys style but not meaning.",
            "remediation": "Replace with semantic tags or use CSS for styling.",
            "wcag_reference": "1.3.1",
            "impact": "Assistive technologies may not interpret styling as meaningful content.",
            "page_url": page_url,
            "element_info": get_element_info(tag)
        })

    # 2️⃣ Detect <div> or <span> used as headers or groups without roles
    for tag in soup.find_all(["div", "span"]):
        if 'header' in tag.get("class", []) or 'heading' in tag.get("class", []):
            raw_incidences.append({
                "title": "Non-semantic container used as header",
                "type": "Semantic Structure",
                "severity": "High",
                "expected_result": "Headings should be marked up using <h1> to <h6>.",
                "actual_result": "A <div> or <span> appears to be used as a header.",
                "remediation": "Replace with the appropriate heading element.",
                "wcag_reference": "1.3.1",
                "impact": "Screen readers may not announce it as a section heading.",
                "page_url": page_url,
                "element_info": get_element_info(tag)
            })

    # 3️⃣ Detect layout tables without headers or scope
    for table in soup.find_all("table"):
        if not table.find("th") and not table.find("caption"):
            raw_incidences.append({
                "title": "Table used for layout without headers",
                "type": "Semantic Structure",
                "severity": "High",
                "expected_result": "Tables must use <th> and <caption> for structure and comprehension.",
                "actual_result": "This table lacks header cells or a caption.",
                "remediation": "Use proper <th> with scope, and provide a <caption>.",
                "wcag_reference": "1.3.1",
                "impact": "Users may not understand how data is related in the table.",
                "page_url": page_url,
                "element_info": get_element_info(table)
            })

    formatted = [format_incidence(inc) for inc in raw_incidences]
    if formatted:
        transform_json_to_excel(formatted, excel)

    return formatted
