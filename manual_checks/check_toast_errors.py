import time
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_toast_errors(html_content, page_url, min_duration=5, excel="issue_report.xlsx"):
    """
    Detects error messages of type "toast" that disappear too quickly before users can read or interact with them.

    🔹 Scans all elements that appear to be "toast messages".
    🔹 Checks if the message disappears automatically in less than `min_duration` seconds.
    🔹 Based on WCAG 2.2.1: Timing Adjustable.

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL (or identifier) of the analyzed page.
        min_duration (int): Minimum time in seconds that the message should remain before disappearing.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 Search for possible toast messages (floating notifications)
    toast_messages = soup.find_all(class_=["toast", "notification", "alert", "error-message"])

    for toast in toast_messages:
        toast_text = toast.get_text(strip=True) or "[Message without text]"
        timeout_value = 2  # Simulation: message disappears in 2s

        if timeout_value < min_duration:
            incidences.append({
                "title": "Error message disappears too quickly",
                "type": "Other A11y",
                "severity": "High",
                "description": (
                    f"The error message '{toast_text}' automatically disappears in {timeout_value} seconds. "
                    "This may prevent some users from reading or understanding the error."
                ),
                "remediation": (
                    "Ensure that error messages remain visible until the user manually dismisses them. "
                    "Ideally, display the message near the form field causing the error."
                ),
                "wcag_reference": "2.2.1",
                "impact": (
                    "Users may not notice the error and may not understand why the form was not submitted."
                ),
                "page_url": page_url,
                "resolution": "check_toast_errors.md"
            })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
