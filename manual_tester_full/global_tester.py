# global_tester.py

import os
import json
from datetime import datetime

from manual_tester_full.check__1_1_1 import run_all___1_1_1
from manual_tester_full.check__1_3_1 import run_all___1_3_1
from manual_tester_full.check__1_3_2 import run_all___1_3_2
from manual_tester_full.check__1_3_3 import run_all___1_3_3
from manual_tester_full.check__1_3_5 import run_all___1_3_5
from manual_tester_full.check__1_4_1 import run_all___1_4_1
from manual_tester_full.check__1_4_3 import run_all___1_4_3
from manual_tester_full.check__1_4_4 import run_all___1_4_4
from manual_tester_full.check__1_4_5 import run_all___1_4_5
from manual_tester_full.check__1_4_10 import run_all___1_4_10
from manual_tester_full.check__1_4_11 import run_all___1_4_11
from manual_tester_full.check__1_4_12 import run_all___1_4_12
from manual_tester_full.check__1_4_13 import run_all___1_4_13
from manual_tester_full.check__2_1_1 import run_all___2_1_1
from manual_tester_full.check__2_1_2 import run_all___2_1_2
from manual_tester_full.check__2_2_1 import run_all___2_2_1
from manual_tester_full.check__2_2_2 import run_all___2_2_2
from manual_tester_full.check__2_4_1 import run_all___2_4_1
from manual_tester_full.check__2_4_2 import run_all___2_4_2
from manual_tester_full.check__2_4_3 import run_all___2_4_3
from manual_tester_full.check__2_4_4 import run_all___2_4_4
from manual_tester_full.check__2_4_6 import run_all___2_4_6
from manual_tester_full.check__2_4_7 import run_all___2_4_7
from manual_tester_full.check__2_5_3 import run_all___2_5_3
from manual_tester_full.check__2_5_7 import run_all___2_5_7
from manual_tester_full.check__2_5_8 import run_all___2_5_8
from manual_tester_full.check__2_4_11 import run_all___2_4_11
from manual_tester_full.check__3_1_1 import run_all___3_1_1
from manual_tester_full.check__3_1_2 import run_all___3_1_2
from manual_tester_full.check__3_2_1 import run_all___3_2_1
from manual_tester_full.check__3_2_2 import run_all___3_2_2
from manual_tester_full.check__3_3_1 import run_all___3_3_1
from manual_tester_full.check__3_3_2 import run_all___3_3_2
from manual_tester_full.check__3_3_3 import run_all___3_3_3
from manual_tester_full.check__3_3_4 import run_all___3_3_4
from manual_tester_full.check__4_1_1 import run_all___4_1_1
from manual_tester_full.check__4_1_2 import run_all___4_1_2
from manual_tester_full.check__4_1_3 import run_all___4_1_3






# Importa cada tester manual
#from manual_checks.check_alt_distinction import check_alt_distinction
#from manual_checks.check_images_decorative import check_images_decorative
#from manual_checks.check_icons_informative import check_icons_informative
#from manual_checks.check_inaccurate_image_text import check_informative_images
#from manual_checks.check_images_of_text import check_images_of_text
#from manual_checks.check_overlay_timeout import check_overlay_timeout
#from manual_checks.check_toast_errors import check_toast_errors
#from manual_checks.check_session_timeout import check_session_timeout
#from manual_checks.check_reflow_320px import check_reflow_320px
#from manual_checks.check_zoom_text_cutoff import check_zoom_text_cutoff
#from manual_checks.check_text_spacing_cropping import check_text_spacing_cropping
#from manual_checks.check_menu_text_spacing import check_menu_text_spacing
#from manual_checks.check_page_title_site_name import check_page_title_site_name_auto_minimal
#from manual_checks.check_page_title_language import check_page_title_language
#from manual_checks.check_tab_aria_selected import check_tab_aria_selected
#from manual_checks.check_button_aria_pressed import check_button_aria_pressed
#from manual_checks.check_accordion_aria_expanded import check_accordion_aria_expanded
#from manual_checks.check_mobile_button_aria_expanded import check_mobile_button_aria_expanded
#from manual_checks.check_button_aria_expanded import check_button_aria_expanded
#from manual_checks.check_combobox_aria_expanded import check_combobox_aria_expanded
#from manual_checks.check_duplicate_ids import check_duplicate_ids
#from manual_checks.check_invalid_elements_in_list import check_invalid_elements_in_list
#from manual_checks.check_aria_label_in_div import check_aria_label_in_div
#from manual_checks.check_buttons_only_by_color import check_buttons_only_by_color
#from manual_checks.check_dropdown_contrast import check_dropdown_contrast
#from manual_checks.check_placeholder_contrast import check_placeholder_contrast
#from manual_checks.check_dropdown_focus_contrast import check_dropdown_focus_contrast
#----------------------------------exam------------------------------------------------
#from manual_checks.check_info_and_relationships import check_info_and_relationships
#from manual_checks.check_keyboard_accessibility import check_keyboard_accessibility
#from manual_checks.check_focus_order import check_focus_order
#from manual_checks.check_focus_visible import check_focus_visible
#from manual_checks.check_form_error_identification import check_form_error_identification
#from manual_checks.check_name_role_value import check_name_role_value
# ... otros testers

# Lista de testers manuales disponibles
TESTERS = [
    # run_all___1_1_1,
    # run_all___1_3_1,
    # run_all___1_3_2,
    # run_all___1_3_3,
    # run_all___1_3_5,
    # run_all___1_4_1,
    # run_all___1_4_3,
    # run_all___1_4_4,
    # run_all___1_4_5,
    # run_all___1_4_10,
    # run_all___1_4_11,
    # run_all___1_4_12,
    # run_all___1_4_13,
    # run_all___2_1_1,
    # run_all___2_1_2,
    run_all___2_2_1,
    # run_all___2_2_2,
    # run_all___2_4_1,
    # run_all___2_4_2,
    # run_all___2_4_3,
    # run_all___2_4_4,
    # run_all___2_4_6,
    # run_all___2_4_7,
    # run_all___2_4_11,
    # run_all___2_5_3,
    # run_all___2_5_7,
    # run_all___2_5_8,
    # run_all___3_1_1,
    # run_all___3_1_2,
    # run_all___3_2_1,
    # run_all___3_2_2,
    # run_all___3_3_1,
    # run_all___3_3_2,
    # run_all___3_3_3,
    # run_all___3_3_4,
    # run_all___4_1_1,
    # run_all___4_1_2,
    # run_all___4_1_3,
    
    
    
    # check_alt_distinction,
    # check_images_decorative,
    # check_icons_informative,
    # check_informative_images,
    # check_images_of_text,
    # check_overlay_timeout,
    # check_toast_errors,
    # check_session_timeout,
    # check_reflow_320px,
    # check_zoom_text_cutoff,
    # check_text_spacing_cropping,
    # check_menu_text_spacing,
    # check_page_title_site_name_auto_minimal,
    # check_page_title_language,
    # check_tab_aria_selected,
    # check_button_aria_pressed,
    # check_accordion_aria_expanded,
    # check_mobile_button_aria_expanded,
    # check_button_aria_expanded,
    # check_combobox_aria_expanded,
    # check_duplicate_ids,
    # check_invalid_elements_in_list,
    # check_aria_label_in_div,
    # check_buttons_only_by_color,
    # check_dropdown_contrast,
    # check_placeholder_contrast,
    # check_dropdown_focus_contrast,
    # #---------------------------------------------------
    # check_info_and_relationships, 
    # check_keyboard_accessibility,
    # check_focus_order,
    # check_focus_visible,
    # check_form_error_identification,
    # check_name_role_value
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
