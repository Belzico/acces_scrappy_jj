import time
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_session_timeout(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if the page properly notifies users about session expiration.

    🔹 Detects if a session timeout warning (modal, alert, etc.) is present.
    🔹 Checks if `aria-live="assertive"` is used to notify screen reader users.
    🔹 Based on WCAG 2.2.1: Timing Adjustable.

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL (or identifier) of the analyzed page.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 1) Check for a session timeout warning
    session_warnings = soup.find_all(class_=["session-warning", "timeout-alert", "modal-warning"])

    if not session_warnings:
        incidences.append({
            "title": "No session timeout warning",
            "type": "Screen Reader",
            "severity": "High",
            "description": (
                "No session timeout warning message was detected before expiration. "
                "Screen reader users may be logged out without prior notice."
            ),
            "remediation": (
                "Implement a warning modal before session expiration with `aria-live='assertive'` "
                "so that users are properly notified."
            ),
            "wcag_reference": "2.2.1",
            "impact": "Users may be locked out without knowing they have been logged out.",
            "page_url": page_url,
            "resolution": "check_session_timeout.md"
        })

    # 🔍 2) Verify if the warning uses `aria-live="assertive"`
    for warning in session_warnings:
        aria_live = warning.get("aria-live", "").lower()
        if aria_live != "assertive":
            incidences.append({
                "title": "Session timeout warning is not screen reader friendly",
                "type": "Screen Reader",
                "severity": "Medium",
                "description": (
                    "A session timeout warning was detected, but it does not use `aria-live='assertive'`, "
                    "which prevents it from being immediately announced to screen reader users."
                ),
                "remediation": (
                    "Add `aria-live='assertive'` to the warning modal or alert."
                ),
                "wcag_reference": "2.2.1",
                "impact": "Users with disabilities will not be notified in time about session expiration.",
                "page_url": page_url,
                "resolution": "check_session_timeout.md"
            })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
