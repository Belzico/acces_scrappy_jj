from bs4 import BeautifulSoup
from collections import defaultdict

def check_duplicate_ids(html_content, page_url):
    """
    Verifica si existen `id` duplicados en el documento HTML.

    - Busca TODOS los elementos con `id` en el documento.
    - Detecta si algún `id` aparece más de una vez.
    - Lista los `id` duplicados y en qué etiquetas se encuentran.
    - Si encuentra duplicados, genera una incidencia.
    """

    # 1) Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Buscar TODOS los elementos con atributo `id`
    id_elements = defaultdict(list)
    for element in soup.find_all(attrs={"id": True}):
        element_id = element["id"]
        tag_name = element.name
        id_elements[element_id].append(tag_name)

    # 3) Filtrar ids duplicados
    duplicated_ids = {id_: tags for id_, tags in id_elements.items() if len(tags) > 1}

    # 4) Generar incidencias si hay `id` duplicados
    incidencias = []
    if duplicated_ids:
        incidencias.append({
            "title": "Duplicated id in fields",
            "type": "HTML Validator",
            "severity": "High",
            "description": (
                "Uno o más elementos en la página tienen el mismo `id`, lo que puede causar "
                "problemas en tecnologías asistivas y scripts de la web. "
                "Cada `id` debe ser único en el DOM."
            ),
            "remediation": (
                "Asegurar que cada `id` en la página sea único. "
                "Si necesitas múltiples instancias, usa `class` o añade un sufijo único, "
                "como `id=\"passwordPositions_1\"`."
            ),
            "wcag_reference": "4.1.1",
            "impact": "Los usuarios que dependen de tecnologías asistivas pueden no recibir el contenido correctamente.",
            "page_url": page_url,
            "duplicated_ids": duplicated_ids  # Listado de los IDs duplicados y en qué etiquetas están
        })

    return incidencias
