from bs4 import BeautifulSoup
from collections import defaultdict
from transform_json_to_excel import transform_json_to_excel  

def check_duplicate_ids(html_content, page_url, excel="issue_report.xlsx"):
    """
    Verifies if there are duplicate `id` attributes in the HTML document.

    - Finds ALL elements with an `id` attribute.
    - Detects if any `id` appears more than once.
    - Lists the duplicated `id` values and their corresponding tags.
    - If duplicates are found, an issue is generated.
    """

    # 1️⃣ Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2️⃣ Find ALL elements with an `id` attribute
    id_elements = defaultdict(list)
    for element in soup.find_all(attrs={"id": True}):
        element_id = element["id"]
        tag_name = element.name
        id_elements[element_id].append(tag_name)

    # 3️⃣ Filter duplicated IDs
    duplicated_ids = {id_: tags for id_, tags in id_elements.items() if len(tags) > 1}

    # 4️⃣ Generate incidences if duplicate `id` values are found
    incidences = []
    if duplicated_ids:
        for id_, tags in duplicated_ids.items():
            incidences.append({
                "title": "Duplicated id in fields",
                "type": "HTML Validator",
                "severity": "High",
                "description": (
                    f"The id `{id_}` is used multiple times in {len(tags)} different elements ({', '.join(tags)}). "
                    "This can cause issues with assistive technologies and web scripts. Each `id` must be unique within the DOM."
                ),
                "remediation": (
                    "Ensure that each `id` in the page is unique. "
                    "If multiple instances are needed, use `class` instead or add a unique suffix, "
                    "e.g., `id='passwordPositions_1'`."
                ),
                "wcag_reference": "4.1.1",
                "impact": "Users relying on assistive technologies may not receive the correct content.",
                "page_url": page_url,
                "resolution": "check_duplicate_ids.md",
                "element_info": str(tags)+"//////"+str(id_)   # List of elements with duplicated IDs
            })

    # Convert incidences to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
