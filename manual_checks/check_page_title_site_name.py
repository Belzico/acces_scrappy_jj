from bs4 import BeautifulSoup
from urllib.parse import urlparse

def check_page_title_site_name_auto_minimal(html_content, page_url):
    """
    Verifica si el título de la página incluye el nombre del sitio web.
    Solo genera incidencia si logra obtener un nombre de sitio
    (sea de og:site_name o dominio) y luego el <title> no lo contiene.

    - No reporta si no existe <title>.
    - No reporta si no se pudo deducir un site_name.
    """

    # 1) Parsear HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Intentar obtener site_name desde meta property="og:site_name"
    og_site = soup.find("meta", property="og:site_name")
    if og_site and og_site.get("content"):
        site_name = og_site["content"].strip()
    else:
        # Si no existe og:site_name, derivar desde dominio
        domain = urlparse(page_url).netloc
        parts = domain.split(".")
        if len(parts) >= 2:
            site_name = parts[-2].capitalize()  # p.ej. "samsclub"
        else:
            # No podemos deducir nada
            site_name = ""

    # 3) Si no se obtuvo un site_name, no reportar
    if not site_name:
        return []

    # 4) Buscar <title>. Si no hay título, no reportar
    title_tag = soup.find("title")
    if not title_tag:
        return []

    title_text = title_tag.get_text(strip=True) or ""
    # 5) Verificar si site_name está en el título
    if site_name.lower() not in title_text.lower():
        return [{
            "title": "Page title does not contain site name",
            "type": "Other A11y",
            "severity": "Medium",
            "description": (
                f"El título de la página '{title_text}' no incluye el sitio '{site_name}'. "
                "Esto dificulta la identificación del sitio por parte del usuario."
            ),
            "remediation": (
                "Actualizar el <title> para que incluya el nombre del sitio web. "
                "Ejemplo: 'Centro de Ayuda - Sams Club'."
            ),
            "wcag_reference": "2.4.2",
            "impact": "Los usuarios no sabrán fácilmente qué sitio están visitando.",
            "page_url": page_url,
        }]
    else:
        return []
