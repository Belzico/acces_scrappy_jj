from bs4 import BeautifulSoup
import re
from transform_json_to_excel import transform_json_to_excel  

# Function to calculate the relative luminance of a color
def luminance(color):
    r, g, b = [int(color[i:i+2], 16) / 255.0 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return (0.2126 * rgb[0]) + (0.7152 * rgb[1]) + (0.0722 * rgb[2])

# Function to calculate the contrast ratio between two colors
def contrast_ratio(color1, color2):
    lum1, lum2 = luminance(color1), luminance(color2)
    return (max(lum1, lum2) + 0.05) / (min(lum1, lum2) + 0.05)

# Main function to detect contrast issues in placeholders
def check_placeholder_contrast(html_content, page_url, excel="issue_report.xlsx"):
    """
    Checks if the placeholder text in `<input>` fields has sufficient contrast against the background.

    - Finds `<input>` fields with a `placeholder` attribute.
    - Extracts text and background colors from `style` attributes if available.
    - Calculates the contrast ratio and reports if it is below 4.5:1.

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL of the analyzed page.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all input fields with a placeholder
    inputs = soup.find_all("input", attrs={"placeholder": True})

    incidences = []
    for input_field in inputs:
        # Extract text and background colors from style attributes if available
        text_color_match = re.search(r'color:\s*(#[0-9A-Fa-f]{6})', input_field.get("style", ""))
        bg_color_match = re.search(r'background-color:\s*(#[0-9A-Fa-f]{6})', input_field.get("style", ""))

        # Default values if colors are not explicitly defined
        text_color = text_color_match.group(1) if text_color_match else "#BFCAD1"  # Default light gray placeholder
        bg_color = bg_color_match.group(1) if bg_color_match else "#FFFFFF"  # Default white background

        # Calculate contrast ratio
        contrast = contrast_ratio(text_color, bg_color)

        if contrast < 4.5:
            incidences.append({
                "title": "Grey placeholder fails contrast on white background",
                "type": "Color Contrast",
                "severity": "High",
                "description": (
                    f"The placeholder text in the input field has a contrast ratio of {contrast:.2f}:1, "
                    "which does not meet the minimum 4.5:1 requirement for small text."
                ),
                "remediation": (
                    "Use a darker color for the placeholder text or change the background to improve contrast. "
                    "Example: `color: #757575;` instead of `color: #BFCAD1;`."
                ),
                "wcag_reference": "1.4.3",
                "impact": "Users with low vision may struggle to read the placeholder text.",
                "page_url": page_url,
                "resolution": "check_placeholder_contrast.md",
                "element_info": str(input_field)
            })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
