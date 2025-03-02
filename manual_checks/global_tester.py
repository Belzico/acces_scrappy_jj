# global_tester.py

import os
import json
from datetime import datetime

# Importa cada tester manual
from manual_checks.check_alt_distinction import check_alt_distinction
from manual_checks.check_images_decorative import check_images_decorative
from manual_checks.check_icons_informative import check_icons_informative
from manual_checks.check_inaccurate_image_text import check_informative_images
from manual_checks.check_images_of_text import check_images_of_text
from manual_checks.check_overlay_timeout import check_overlay_timeout
from manual_checks.check_toast_errors import check_toast_errors
from manual_checks.check_session_timeout import check_session_timeout
from manual_checks.check_reflow_320px import check_reflow_320px
from manual_checks.check_zoom_text_cutoff import check_zoom_text_cutoff
from manual_checks.check_text_spacing_cropping import check_text_spacing_cropping
from manual_checks.check_menu_text_spacing import check_menu_text_spacing
from manual_checks.check_page_title_site_name import check_page_title_site_name_auto_minimal
from manual_checks.check_page_title_language import check_page_title_language
from manual_checks.check_tab_aria_selected import check_tab_aria_selected
# ... otros testers

# Lista de testers manuales disponibles
TESTERS = [
    check_alt_distinction,
     check_images_decorative,
     check_icons_informative,
     check_informative_images,
     check_images_of_text,
     check_overlay_timeout,
     check_toast_errors,
     check_session_timeout,
     check_reflow_320px,
     check_zoom_text_cutoff,
     check_text_spacing_cropping,
     check_menu_text_spacing,
     check_page_title_site_name_auto_minimal,
     check_page_title_language,
     check_tab_aria_selected,
    # ...
]

def run_all_testers(html_content, page_url):
    """
    Ejecuta todos los testers manuales sobre el contenido HTML (un único documento)
    y devuelve las incidencias encontradas.
    """
    all_incidencias = []
    for tester in TESTERS:
        incidencias = tester(html_content, page_url)
        all_incidencias.extend(incidencias)
    return all_incidencias

def run_all_testers_in_folder(folder_path):
    """
    NUEVA FUNCIÓN:
    1) Busca todos los archivos .html en 'folder_path'.
    2) Para cada .html, lo abre, obtiene su contenido,
       y llama a 'run_all_testers'.
    3) Retorna la lista total de incidencias de la carpeta.
    """
    if not os.path.isdir(folder_path):
        print(f"🚫 {folder_path} no es una carpeta válida.")
        return []

    html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]
    if not html_files:
        print(f"⚠️ No se encontraron archivos .html en {folder_path}")
        return []

    all_folder_incidences = []
    for file_name in html_files:
        file_path = os.path.join(folder_path, file_name)
        # Leemos el contenido HTML
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
            continue

        # Llamamos al tester manual
        incidences = run_all_testers(content, page_url=file_path)
        all_folder_incidences.extend(incidences)

    return all_folder_incidences

def report_incidences_to_file(incidencias, report_file="manual_incidences.json"):
    """
    Guarda las incidencias en un archivo JSON (append).
    """
    existing_data = []
    if os.path.isfile(report_file):
        try:
            with open(report_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

    now_str = datetime.now().isoformat()
    for inc in incidencias:
        inc["detected_at"] = now_str

    existing_data.extend(incidencias)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
