from bs4 import BeautifulSoup
from urllib.parse import urlparse
from transform_json_to_excel import transform_json_to_excel  

def check_page_title_site_name_auto_minimal(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if the page title includes the website name.
    Only generates an issue if a site name is detected
    (either from og:site_name or the domain) and the <title> does not contain it.

    - Does not report if <title> is missing.
    - Does not report if a site name cannot be determined.

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL of the analyzed page.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    incidences = []
    
    # 1) Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Attempt to get site_name from meta property="og:site_name"
    og_site = soup.find("meta", property="og:site_name")
    if og_site and og_site.get("content"):
        site_name = og_site["content"].strip()
    else:
        # If og:site_name does not exist, derive from domain
        domain = urlparse(page_url).netloc
        parts = domain.split(".")
        if len(parts) >= 2:
            site_name = parts[-2].capitalize()  # e.g., "samsclub"
        else:
            # Cannot determine site name
            site_name = ""

    # 3) If no site_name is obtained, do not report
    if not site_name:
        return []

    # 4) Find <title>. If missing, do not report
    title_tag = soup.find("title")
    if not title_tag:
        return []

    title_text = title_tag.get_text(strip=True) or ""

    # 5) Check if site_name is included in the title
    if site_name.lower() not in title_text.lower():
        incidences.append({
            "title": "Page title does not contain site name",
            "type": "Other A11y",
            "severity": "Medium",
            "description": (
                f"The page title '{title_text}' does not include the site name '{site_name}'. "
                "This makes it harder for users to identify the website."
            ),
            "remediation": (
                "Update the <title> to include the site name. "
                "Example: 'Help Center - Sams Club'."
            ),
            "wcag_reference": "2.4.2",
            "impact": "Users may not easily recognize which site they are visiting.",
            "page_url": page_url,
            "resolution": "check_page_title_site_name_auto_minimal.md"
        })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
