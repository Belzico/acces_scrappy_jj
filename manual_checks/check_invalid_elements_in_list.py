from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def get_element_info(element):
    """Retrieves useful information about an HTML element to facilitate issue identification."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # First 50 characters of the text
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"
    }

def check_invalid_elements_in_list(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if `<div>` elements are directly nested inside `<ul>` or `<ol>` lists.

    - Finds all `<ul>` and `<ol>` elements.
    - Checks if they contain `<div>` elements directly inside them.
    - If invalid elements are found, an issue is generated.
    """

    # 1️⃣ Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2️⃣ Find all `<ul>` and `<ol>` lists
    list_elements = soup.find_all(["ul", "ol"])

    # 3️⃣ Find `<div>` elements directly inside `<ul>` or `<ol>` without a `<li>` container
    invalid_lists = []
    for lst in list_elements:
        for child in lst.find_all(recursive=False):  # Only direct children
            if child.name == "div":
                invalid_lists.append(child)

    # 4️⃣ Generate incidences if `<div>` elements are found inside `<ul>` or `<ol>`
    incidences = []
    for invalid in invalid_lists:
        incidences.append({
            "title": "Div elements nested inside ul/ol in the navigation menu",
            "type": "HTML Validator",
            "severity": "Low",
            "description": (
                "A `<ul>` or `<ol>` element should not contain `<div>` elements as direct children. "
                "Only `<li>`, `<script>`, or `<template>` are allowed inside lists."
            ),
            "remediation": (
                "Ensure that `<div>` elements inside `<ul>` or `<ol>` are wrapped in `<li>`. "
                "Example: `<li><div class=\"menu-item\">Home</div></li>`."
            ),
            "wcag_reference": "4.1.1",
            "impact": "No immediate impact, but it may cause validation issues and future compatibility problems.",
            "page_url": page_url,
            "resolution": "check_invalid_elements_in_list.md",
            "element_info": get_element_info(invalid)
        })

    # Convert incidences to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
