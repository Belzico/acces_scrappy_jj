from bs4 import BeautifulSoup
import langid
from collections import Counter

def extract_visible_text_elements(soup):
    """
    Extrae una lista de textos visibles de la página,
    excluyendo scripts, estilos y meta tags.
    """
    blacklist = {"script", "style", "noscript", "meta", "head", "link"}
    texts = [
        element.get_text(strip=True) 
        for element in soup.find_all() 
        if element.name not in blacklist and element.get_text(strip=True)
    ]
    return texts  # Lista de fragmentos de texto individuales

def check_page_title_language(html_content, page_url, threshold=0.2):
    """
    Verifica si más del 20% del contenido visible de la página está en un idioma diferente al definido en <html lang="xx">.
    
    - Se obtiene el idioma desde <html lang="xx">.
    - Se analiza cada bloque de texto visible con fastText/langid.
    - Si más del 20% del contenido no coincide con el idioma esperado, se reporta una incidencia.
    """

    # 1) Parsear HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Obtener el atributo lang de <html>
    html_tag = soup.find("html")
    if not html_tag or not html_tag.has_attr("lang"):
        return []  # No hay lang definido, no podemos hacer la verificación

    expected_lang = html_tag["lang"].strip().lower()  # Ejemplo: "es", "en", "fr"

    # 3) Extraer lista de textos visibles del documento
    text_elements = extract_visible_text_elements(soup)
    total_fragments = len(text_elements)
    if total_fragments == 0:
        return []  # No hay texto visible para analizar

    detected_languages = []  # Lista para almacenar los idiomas detectados

    # 4) Analizar cada fragmento de texto individualmente con fastText/langid
    for text in text_elements:
        if len(text) < 5:  # Evitamos detectar idioma en textos muy cortos
            continue
        
        detected_lang, confidence = langid.classify(text)  # Devuelve el idioma más probable

        # Agregar solo si la confianza es alta (> 80%)
        if confidence > 0.8:
            detected_languages.append(detected_lang)

    # 5) Contar ocurrencias de cada idioma detectado
    lang_counts = Counter(detected_languages)
    total_detected = sum(lang_counts.values())

    # 6) Calcular porcentaje de idiomas distintos al esperado
    incorrect_texts = total_detected - lang_counts.get(expected_lang, 0)
    incorrect_percentage = incorrect_texts / total_detected if total_detected > 0 else 0

    # 7) Si más del 20% del contenido no coincide con el idioma esperado, generamos una incidencia
    incidencias = []
    if incorrect_percentage > threshold:
        incidencias.append({
            "title": "Page language mismatch",
            "type": "Other A11y",
            "severity": "High",
            "description": (
                f"Se detectó que el {incorrect_percentage:.1%} del contenido visible de la página está en un idioma diferente a '{expected_lang}' definido en <html lang>.\n"
                f"Idiomas detectados: {dict(lang_counts)}"
            ),
            "remediation": (
                f"Revisar el idioma principal del contenido. Si la página está en '{expected_lang}', "
                "asegúrate de que al menos el 80% del contenido visible coincida con ese idioma."
            ),
            "wcag_reference": "3.1.1",
            "impact": (
                "Los usuarios con lectores de pantalla podrían recibir una pronunciación incorrecta "
                "si el contenido está en un idioma diferente al definido en la página."
            ),
            "page_url": page_url,
        })

    return incidencias
