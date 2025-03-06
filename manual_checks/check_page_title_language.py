from bs4 import BeautifulSoup
import langid
from collections import Counter
from transform_json_to_excel import transform_json_to_excel  

def extract_visible_text_elements(soup):
    """
    Extracts a list of visible text elements from the page,
    excluding scripts, styles, and meta tags.
    """
    blacklist = {"script", "style", "noscript", "meta", "head", "link"}
    texts = [
        element.get_text(strip=True) 
        for element in soup.find_all() 
        if element.name not in blacklist and element.get_text(strip=True)
    ]
    return texts  # List of individual text fragments

def check_page_title_language(html_content, page_url, threshold=0.2, excel="issue_report.xlsx"):
    """
    Checks if more than 20% of the visible content is in a language different from the one defined in <html lang="xx">.
    
    - Retrieves the language from <html lang="xx">.
    - Analyzes each visible text block using fastText/langid.
    - If more than 20% of the content does not match the expected language, an issue is reported.

    Args:
        html_content (str): HTML content of the page.
        page_url (str): URL of the analyzed page.
        threshold (float): Percentage of incorrect language content allowed before reporting an issue.
        excel (str): Path to save the issue report in Excel format.

    Returns:
        list[dict]: List of detected issues.
    """

    # 1) Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Get the lang attribute from <html>
    html_tag = soup.find("html")
    if not html_tag or not html_tag.has_attr("lang"):
        return []  # No lang defined, verification cannot be performed

    expected_lang = html_tag["lang"].strip().lower()  # Example: "es", "en", "fr"

    # 3) Extract a list of visible text elements from the document
    text_elements = extract_visible_text_elements(soup)
    total_fragments = len(text_elements)
    if total_fragments == 0:
        return []  # No visible text to analyze

    detected_languages = []  # List to store detected languages

    # 4) Analyze each text fragment individually with langid
    for text in text_elements:
        if len(text) < 5:  # Avoid detecting language in very short texts
            continue
        
        detected_lang, confidence = langid.classify(text)  # Returns the most probable language

        # Add only if confidence is high (> 80%)
        if confidence > 0.8:
            detected_languages.append(detected_lang)

    # 5) Count occurrences of each detected language
    lang_counts = Counter(detected_languages)
    total_detected = sum(lang_counts.values())

    # 6) Calculate the percentage of texts in a different language than expected
    incorrect_texts = total_detected - lang_counts.get(expected_lang, 0)
    incorrect_percentage = incorrect_texts / total_detected if total_detected > 0 else 0

    # 7) If more than 20% of the content does not match the expected language, generate an issue
    incidences = []
    if incorrect_percentage > threshold:
        incidences.append({
            "title": "Page language mismatch",
            "type": "Other A11y",
            "severity": "High",
            "description": (
                f"{incorrect_percentage:.1%} of the visible content on the page is in a language different from '{expected_lang}' defined in <html lang>.\n"
                f"Detected languages: {dict(lang_counts)}"
            ),
            "remediation": (
                f"Review the primary language of the content. If the page is in '{expected_lang}', "
                "ensure that at least 80% of the visible content matches that language."
            ),
            "wcag_reference": "3.1.1",
            "impact": (
                "Users with screen readers may receive incorrect pronunciation "
                "if the content is in a different language than defined on the page."
            ),
            "page_url": page_url,
            "resolution": "check_page_title_language.md"
        })

    # Convert incidences directly to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
