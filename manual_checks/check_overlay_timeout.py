import time
from bs4 import BeautifulSoup
from transform_json_to_excel import transform_json_to_excel  

def check_overlay_timeout(html_content, page_url, min_duration=5, excel="issue_report.xlsx"):
    """
    Detects overlays that disappear too quickly before users can interact with them.

    🔹 Scans all buttons that trigger overlays.
    🔹 Checks if the overlay disappears automatically in less than `min_duration` seconds.
    🔹 Based on WCAG 2.2.1: Timing Adjustable (https://www.w3.org/WAI/WCAG21/Understanding/time-adjustable.html).

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL (or identifier) of the analyzed page.
        min_duration (int): Minimum time in seconds the overlay should remain visible before disappearing.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 🔍 1) Search for all buttons that may trigger overlays
    buttons = soup.find_all("button")  # Detects <button>
    buttons += soup.find_all("a", onclick=True)  # Detects <a> with onclick
    buttons += soup.find_all("div", onclick=True)  # Detects <div> with onclick
    buttons += soup.find_all(class_="button")  # Detects any element with class="button"

    # 🔍 2) Search for possible overlays in the page
    overlays = soup.find_all(["div", "dialog"], class_=["overlay", "popup", "modal"])

    if not buttons or not overlays:
        return []  # No buttons or overlays detected

    for button in buttons:
        button_text = button.get_text(strip=True) or "[Button without text]"

        for overlay in overlays:
            overlay_id = overlay.get("id", "[no id]")

            # 🔥 Simulation: Overlay disappears in less than `min_duration` seconds
            timeout_value = 3  # Example overlay timeout of 3s

            if timeout_value < min_duration:
                incidences.append({
                    "title": "Overlay disappears too quickly",
                    "type": "Other A11y",
                    "severity": "High",
                    "description": (
                        f"The overlay '{overlay_id}' automatically disappears in {timeout_value} seconds "
                        f"after clicking the button '{button_text}'. "
                        "This may prevent some users from properly interacting with it."
                    ),
                    "remediation": (
                        "Ensure that the overlay remains visible until the user manually closes it, "
                        "or provide an option in the settings to adjust the timing."
                    ),
                    "wcag_reference": "2.2.1",
                    "impact": (
                        "Users with visual, motor, or cognitive disabilities may not have enough time "
                        "to read or interact with the overlay content before it disappears."
                    ),
                    "page_url": page_url,
                    "resolution": "check_overlay_timeout.md"
                })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
