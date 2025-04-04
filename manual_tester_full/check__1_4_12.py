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
    line_number = element.sourceline if hasattr(element, 'sourceline') else "N/A"

    evidence_parts = []
    if classes:
        evidence_parts.append(f"class={classes}")
    if element_id:
        evidence_parts.append(f"id={element_id}")
    if line_number != "N/A":
        evidence_parts.append(f"line={line_number}")

    evidence_str = ", ".join(evidence_parts)
    evidence = f"{tag}[{evidence_str}]" if evidence_parts else tag

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
        "fragment_html": snippet_str
    }


def format_incidence(issue):
    element_info = issue.get("element_info", {})
    snippet = element_info.get("fragment_html", "")

    return {
        "Title": issue.get("title"),
        "Steps": (
            f"1. Open the page: {issue.get('page_url')}\n"
            f"2. Inspect the element: {element_info.get('tag', 'N/A')}\n"
            f"3. Review its inline styles affecting spacing.\n\n"
            f"HTML snippet (around line {element_info.get('line_number', 'N/A')}):\n"
            f"{snippet}"
        ),
        "Bug Type": issue.get("type"),
        "Priority": issue.get("severity"),
        "Expected Result": issue.get("expected_result", "N/A"),
        "Actual Result": issue.get("actual_result", "N/A"),
        "Suggested resolution(s)": issue.get("remediation"),
        "Failed checkpoint": issue.get("wcag_reference"),
        "User Impact": issue.get("impact"),
        "Evidence [SS or Video]": element_info.get("evidence", "N/A")
    }


def run_all___1_4_12(html_content, page_url, excel="issue_report.xlsx"):
    soup = BeautifulSoup(html_content, "html.parser")
    lines = get_html_lines(html_content)
    incidences = []

    # === Check 1: Menús ===
    menus = soup.find_all(["nav", "ul", "div"], class_=["menu", "navigation", "navbar"])

    for menu in menus:
        for item in menu.find_all(["li", "a", "span", "div"]):
            style = item.get("style", "").lower()
            info = get_element_info(item, html_lines=lines)

            if "overflow: hidden" in style:
                incidences.append(format_incidence({
                    "title": "Content may be cropped with text spacing adjustments",
                    "type": "Zoom",
                    "severity": "High",
                    "expected_result": "Text containers should expand when spacing is increased.",
                    "actual_result": "This menu item uses `overflow: hidden;`, which may cut off content.",
                    "remediation": "Avoid using `overflow: hidden;` in menu items.",
                    "wcag_reference": "1.4.12",
                    "impact": "Users may not see the full menu content with larger spacing.",
                    "page_url": page_url,
                    "element_info": info
                }))

            if "white-space: nowrap" in style:
                incidences.append(format_incidence({
                    "title": "Text does not wrap in the menu",
                    "type": "Zoom",
                    "severity": "High",
                    "expected_result": "Text should wrap naturally when spacing increases.",
                    "actual_result": "This menu item uses `white-space: nowrap;`, preventing wrapping.",
                    "remediation": "Allow wrapping to avoid overflow issues.",
                    "wcag_reference": "1.4.12",
                    "impact": "Menu items may overflow or be unreadable.",
                    "page_url": page_url,
                    "element_info": info
                }))

            if "max-height" in style and "px" in style:
                incidences.append(format_incidence({
                    "title": "Menu items may be cut off",
                    "type": "Zoom",
                    "severity": "High",
                    "expected_result": "Menus should expand when spacing increases.",
                    "actual_result": "A menu item uses `max-height` in pixels, risking truncation.",
                    "remediation": "Use `min-height: auto;` or flexible sizing.",
                    "wcag_reference": "1.4.12",
                    "impact": "Text may become unreadable.",
                    "page_url": page_url,
                    "element_info": info
                }))

    # === Check 2: Text containers generales ===
    text_containers = soup.find_all(["p", "div", "span", "section", "article"], style=True)
    overflow_hidden_regex = re.compile(r"overflow(?:-x|-y)?\s*:\s*hidden", re.IGNORECASE)
    height_fixed_regex = re.compile(r"height\s*:\s*\d+px", re.IGNORECASE)

    for element in text_containers:
        style_attr = element.get("style", "").lower()
        info = get_element_info(element, html_lines=lines)

        if overflow_hidden_regex.search(style_attr):
            incidences.append(format_incidence({
                "title": "Content may be cropped with text spacing adjustments",
                "type": "Zoom",
                "severity": "High",
                "expected_result": "Text containers should be allowed to grow when spacing increases.",
                "actual_result": "This element uses `overflow: hidden;`, which may crop content.",
                "remediation": "Avoid overflow:hidden; or use `overflow: visible;` for text containers.",
                "wcag_reference": "1.4.12",
                "impact": "Users may miss important content.",
                "page_url": page_url,
                "element_info": info
            }))

        if height_fixed_regex.search(style_attr):
            incidences.append(format_incidence({
                "title": "Fixed height detected, may crop text",
                "type": "Zoom",
                "severity": "High",
                "expected_result": "Heights should be dynamic or use min-height to allow spacing flexibility.",
                "actual_result": "This element uses fixed height (`height: XXpx;`), risking content cutoff.",
                "remediation": "Use `min-height: auto;` or relative units.",
                "wcag_reference": "1.4.12",
                "impact": "Text may be truncated when spacing increases.",
                "page_url": page_url,
                "element_info": info
            }))

    if incidences:
        transform_json_to_excel(incidences, excel)

    return incidences
