# file: check_alt_distinction.py

from bs4 import BeautifulSoup, NavigableString
from sentence_transformers import SentenceTransformer, util
from transform_json_to_excel import transform_json_to_excel  

# Load the transformer model for semantic similarity
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_element_info(element):
    """Retrieves useful information about an HTML element to facilitate issue identification."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # First 50 characters of the text
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"
    }

def check_alt_distinction(html_content, page_url, excel="issue_report.xlsx", similarity_threshold=0.8):
    """
    Checks for missing or redundant alt attributes in images:
    
    1) Missing alt (error).
    2) Empty alt (`alt=""`), potentially decorative:
       - If inside a link/button with no text or aria-label, it's an error.
    3) Non-empty alt (likely informative):
       - Semantically compared with nearby text using Sentence Transformers.
       - If similarity > threshold, it's considered redundant.

    Args:
      html_content (str): HTML content of the page.
      page_url (str): URL (or identifier) of the page.
      similarity_threshold (float): Cosine similarity threshold for redundancy detection.

    Returns:
      list[dict]: List of detected issues.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    incidences = []

    images = soup.find_all("img")

    for img in images:
        src = img.get("src", "")
        alt = img.get("alt", None)  # None if missing
        parent = img.parent  # Immediate parent, e.g., <a> or <p>...

        # 1️⃣ IMAGE MISSING ALT ATTRIBUTE
        if alt is None:
            incidences.append({
                "title": "Image missing alt attribute",
                "type": "Alternative Text",
                "severity": "High",
                "description": "This image does not have an alt attribute. "
                               "It is unclear whether it is decorative or informative. "
                               "Screen readers may announce the filename instead.",
                "remediation": "Add an appropriate alt attribute. "
                               "If decorative, use `alt=''` and `aria-hidden='true'`. "
                               "If informative, describe the image content in alt.",
                "wcag_reference": "1.1.1",
                "impact": "Screen reader users may not understand the image's purpose.",
                "page_url": page_url,
                "resolution": "check_alt_distinction.md",
                "element_info": get_element_info(img)
            })
            continue

        # 2️⃣ IMAGE WITH EMPTY ALT (`alt=""`) - POTENTIALLY DECORATIVE
        if alt.strip() == "":
            if parent and parent.name in ["a", "button"]:
                link_text = "".join(parent.stripped_strings)
                aria_label = parent.get("aria-label", "")

                if not link_text and not aria_label:
                    incidences.append({
                        "title": "Link/Button with no accessible text",
                        "type": "Alternative Text",
                        "severity": "High",
                        "description": "The image has `alt=''`, suggesting it is decorative, "
                                       "but it is the only content inside a link/button with no text or aria-label. "
                                       "Screen reader users will not know the function of the link.",
                        "remediation": "Add accessible text, e.g., `aria-label='Go to homepage'` "
                                       "or visible text inside the link.",
                        "wcag_reference": "1.1.1",
                        "impact": "Screen reader users will not know the purpose of this link or button.",
                        "page_url": page_url,
                        "resolution": "check_alt_distinction.md",
                        "element_info": get_element_info(parent)
                    })
            continue  # Skip further checks if the alt is empty and not inside an invalid container.

        # 3️⃣ IMAGE WITH NON-EMPTY ALT - CHECK FOR REDUNDANCY
        alt_text = alt.strip()

        # Extract adjacent text (previous and next text nodes)
        previous_text = img.find_previous(string=True, recursive=True)
        next_text = img.find_next(string=True, recursive=True)

        previous_text = previous_text.strip() if previous_text else ""
        next_text = next_text.strip() if next_text else ""

        adjacent_text = f"{previous_text} {next_text}".strip()

        if adjacent_text:
            # Convert to embeddings
            alt_embedding = model.encode(alt_text, convert_to_tensor=True)
            adj_embedding = model.encode(adjacent_text, convert_to_tensor=True)

            # Compute cosine similarity
            similarity = util.cos_sim(alt_embedding, adj_embedding).item()

            if similarity > similarity_threshold:
                incidences.append({
                    "title": "Redundant alternative text (semantic match)",
                    "type": "Alternative Text",
                    "severity": "Medium",
                    "description": f"The image's alt text appears redundant with nearby text "
                                   f"(semantic similarity={similarity:.2f}). "
                                   "This may cause screen reader users to hear the same information twice.",
                    "remediation": "If the image is purely decorative, use `alt=''`. "
                                   "If informative, ensure the alt provides additional information "
                                   "not already conveyed in nearby text.",
                    "wcag_reference": "1.1.1",
                    "impact": "Screen reader users may receive duplicate information.",
                    "page_url": page_url,
                    "resolution": "check_alt_distinction.md",
                    "element_info": get_element_info(img)
                })

    # Convert incidences to Excel before returning
    transform_json_to_excel(incidences, excel)

    return incidences
