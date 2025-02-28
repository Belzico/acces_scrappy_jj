# file: check_alt_distinction.py

from bs4 import BeautifulSoup, NavigableString
from sentence_transformers import SentenceTransformer, util

# Carga el modelo al inicio del script (o en lazy load si prefieres).
# "all-MiniLM-L6-v2" es un modelo pequeño y rápido.
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def check_alt_distinction(html_content, page_url, similarity_threshold=0.8):
    """
    Verifica imágenes para diferenciar:
    1) Falta de alt (error seguro).
    2) alt="" (potencialmente decorativa):
       - Si está en un enlace SIN texto ni aria-label, es un error.
    3) alt con texto (probablemente informativa):
       - Se compara SEMÁNTICAMENTE con texto adyacente usando Sentence Transformers.
       - Si la similitud es > similarity_threshold, se considera redundante.

    Args:
      html_content (str): contenido HTML de la página.
      page_url (str): URL (o identificador) de la página.
      similarity_threshold (float): Umbral de similitud coseno para considerar "redundante".

    Returns:
      list[dict]: Lista de incidencias detectadas.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    incidencias = []

    images = soup.find_all("img")

    for img in images:
        src = img.get("src", "")
        alt = img.get("alt", None)  # Si no existe, retorna None
        parent = img.parent  # Padre inmediato, p.ej. <a> o <p>...

        # 1) IMAGEN SIN ALT -> ERROR DIRECTO
        if alt is None:
            incidencias.append({
                "title": "Imagen sin atributo alt",
                "page": page_url,
                "element": f"<img src='{src}'>",
                "description": (
                    "Esta imagen no tiene atributo alt. "
                    "Se desconoce si es decorativa o informativa. "
                    "Los lectores de pantalla podrían anunciar el nombre de archivo."
                ),
                "wcag": "1.1.1",
                "suggested_fix": (
                    "Agregar alt apropiado. "
                    "Si es decorativa, usar alt='' y aria-hidden='true'. "
                    "Si es informativa, describir su contenido en alt."
                )
            })
            continue

        # 2) IMAGEN CON alt="" (posiblemente decorativa)
        if alt.strip() == "":
            # Verificamos si la imagen está en un <a> o <button> sin texto ni aria-label
            if parent and parent.name in ["a", "button"]:
                link_text = "".join(parent.stripped_strings)
                aria_label = parent.get("aria-label", "")

                if not link_text and not aria_label:
                    incidencias.append({
                        "title": "Enlace/Botón sin texto accesible",
                        "page": page_url,
                        "element": str(parent),
                        "description": (
                            "La imagen tiene alt='', indicando que es decorativa, "
                            "pero es el único contenido de un enlace/botón sin texto ni aria-label. "
                            "El usuario de lector de pantalla no sabrá la función del enlace."
                        ),
                        "wcag": "1.1.1",
                        "suggested_fix": (
                            "Agregar un texto accesible. "
                            "Ej: aria-label='Ir a inicio' o un texto dentro del enlace."
                        )
                    })
            # Caso contrario, alt="" es correcto o no, depende de revisión humana.
            continue

        # 3) IMAGEN CON alt NO VACÍO (probablemente informativa)
        # Vamos a comparar SEMÁNTICAMENTE con texto adyacente.
        alt_text = alt.strip()

        # Extraer texto adyacente (anterior y siguiente nodo de texto)
        previous_text = img.find_previous(string=True, recursive=True)
        next_text = img.find_next(string=True, recursive=True)

        # Limpiamos
        previous_text = ""
        if img.previous_sibling and isinstance(img.previous_sibling, NavigableString):
            previous_text = img.previous_sibling.strip()

        next_text = ""
        if img.next_sibling and isinstance(img.next_sibling, NavigableString):
            next_text = img.next_sibling.strip()

        # Puedes concatenar ambos para tener un "texto cercano" unificado
        adjacent_text = f"{previous_text} {next_text}".strip()

        # Comparamos sólo si hay al menos algo de texto en adjacent_text
        if adjacent_text:
            # Convertimos a embeddings
            alt_embedding = model.encode(alt_text, convert_to_tensor=True)
            adj_embedding = model.encode(adjacent_text, convert_to_tensor=True)

            # Calculamos la similitud coseno
            similarity = util.cos_sim(alt_embedding, adj_embedding).item()  # .item() saca float

            if similarity > similarity_threshold:
                # Se considera redundante
                incidencias.append({
                    "title": "Texto alternativo redundante (semánticamente)",
                    "page": page_url,
                    "element": f"<img src='{src}' alt='{alt_text}'>",
                    "description": (
                        "El texto alternativo de la imagen parece redundar con el texto cercano "
                        f"(similaridad semántica={similarity:.2f}). Esto podría causar que usuarios "
                        "de lectores de pantalla escuchen la misma información dos veces."
                    ),
                    "wcag": "1.1.1",
                    "suggested_fix": (
                        "Si la imagen es meramente decorativa, usar alt=''. "
                        "Si es informativa, use un alt que aporte información adicional y no repita "
                        "lo ya dicho en el texto cercano."
                    )
                })

    return incidencias
