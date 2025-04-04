import json
import asyncio
import os
from bs4 import BeautifulSoup

# ==== IMPORTACIONES DE TUS MÓDULOS EXISTENTES ====
from scraper.scraper import WebScraper
from accessibility_checker.axe_checker import analyze_accessibility, analyze_local_html
from accessibility_checker.lighthouse_checker import analyze_lighthouse  # 🔥 NUEVO
from reports.generate_report import generate_report

# from manual_checks.global_tester import (
#     run_all_testers,
#     run_all_testers_in_folder,
#     report_incidences_to_file
# )

from manual_tester_full.global_tester import (
    run_all_testers,
    run_all_testers_in_folder,
    report_incidences_to_file
)

# =============================================================================
# 1) Función que ejecuta TODO el proceso de scraping y análisis
# =============================================================================

async def run_full_analysis(start_url: str, class_list=None):
    """
    Ejecuta todo el scraping y análisis de accesibilidad para la URL dada.
    
    :param start_url: La URL base a scrapear.
    :param class_list: Lista de clases (strings) para filtrar contenido.
                       Si es None o está vacía, no se filtra por clase.
    """
    if class_list is None:
        class_list = []

    print(f"\n=== Análisis para URL: {start_url} con clases: {class_list} ===")

    # 1) Scraping
    print("🔍 Scrapeando el sitio web...")
    scraper = WebScraper(start_url)
    pages = await scraper.run()

    # 2) Configuración de listas para recolección de resultados
    print("🧪 Analizando accesibilidad de las páginas vivas...")
    axe_results = []
    lighthouse_errors = []  # 🔥 Aquí guardamos SOLO los errores de Lighthouse
    all_manual_incidences = []

    # -------------------------------------------------------------------------
    # 3) Recorrer las páginas vivas extraídas por el scraper
    # -------------------------------------------------------------------------
    for page in pages:
        page_url = page["url"]
        print(f"Procesando página: {page_url}")

        # --- 3.1) Análisis con axe-core ---
        accessibility_result = await analyze_accessibility(page_url)
        axe_results.append(accessibility_result)

        # --- 3.2) Análisis con Lighthouse (solo errores) ---
        lighthouse_result = analyze_lighthouse(page_url)  # 🔥 NUEVO
        if lighthouse_result:
            lighthouse_errors.extend(lighthouse_result)  # Guardamos solo errores

        # --- 3.3) Chequeo manual ---
        html_content = page.get("content", "")
        if not html_content:
            print(f"⚠️ No hay contenido HTML en {page_url} para pruebas manuales.")
            continue

        # Si tenemos clases definidas, filtramos por cada clase individual y 
        # ejecutamos los tests manuales con el contenido filtrado.
        if class_list:
            for target_class in class_list:
                soup = BeautifulSoup(html_content, "html.parser")
                target_elements = soup.find_all(class_=target_class)
                filtered_content = "".join(str(el) for el in target_elements)

                if not filtered_content.strip():
                    print(f"⚠️ No se encontró la clase '{target_class}' en {page_url}. Omitiendo.")
                    continue

                # Ejecutar testers manuales
                manual_incidences = run_all_testers(filtered_content, page_url)
                if manual_incidences:
                    all_manual_incidences.extend(manual_incidences)
                    report_incidences_to_file(manual_incidences, "manual_incidences.json")
        else:
            # Si NO hay clases definidas, se hace el test sobre TODO el HTML
            manual_incidences = run_all_testers(html_content, page_url)
            if manual_incidences:
                all_manual_incidences.extend(manual_incidences)
                report_incidences_to_file(manual_incidences, "manual_incidences.json")

    # -------------------------------------------------------------------------
    # 4) Guardar resultados de AXE y Lighthouse
    # -------------------------------------------------------------------------
    with open("accessibility_results.json", "w", encoding="utf-8") as f:
        json.dump(axe_results, f, indent=4, ensure_ascii=False)

    with open("lighthouse_errors.json", "w", encoding="utf-8") as f:
        json.dump(lighthouse_errors, f, indent=4, ensure_ascii=False)

    print("📊 Generando reporte de accesibilidad...")
    generate_report(axe_results)

    # -------------------------------------------------------------------------
    # 5) Análisis de archivos locales (html_samples)
    # -------------------------------------------------------------------------
    local_folder = "C:\\Users\\namic\\OneDrive\\Documentos\\GitHub\\acces_scrappy_jj\\html_samples"
    if os.path.isdir(local_folder):
        print(f"\n🗂  Analizando carpeta local: {local_folder}")

        # --- 5.1) Análisis local con axe ---
        local_analysis_results = await analyze_local_html(local_folder)
        axe_results.extend(local_analysis_results)

        # --- 5.2) Testers manuales en cada archivo HTML ---
        folder_incidences = []
        for file_name in os.listdir(local_folder):
            if file_name.endswith(".html"):
                file_path = os.path.join(local_folder, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if class_list:
                    for target_class in class_list:
                        soup = BeautifulSoup(content, "html.parser")
                        target_elements = soup.find_all(class_=target_class)
                        filtered_content = "".join(str(el) for el in target_elements)

                        if not filtered_content.strip():
                            print(f"⚠️ No se encontró la clase '{target_class}' en {file_name}. Omitiendo.")
                            continue

                        incidences = run_all_testers(filtered_content, file_path)
                        folder_incidences.extend(incidences)
                else:
                    # Sin clases: prueba el HTML completo
                    incidences = run_all_testers(content, file_path)
                    folder_incidences.extend(incidences)

        # Si encontramos incidencias manuales, las agregamos y reportamos
        if folder_incidences:
            all_manual_incidences.extend(folder_incidences)
            report_incidences_to_file(folder_incidences, "manual_incidences.json")

    print("✅ Finalizado. Revisa 'accessibility_results.json', 'lighthouse_errors.json' y 'manual_incidences.json'.")

# =============================================================================
# 2) Función main: Invoca a run_full_analysis para múltiples URLs y clases
# =============================================================================

async def main():
    """
    Aquí definimos cada URL y las clases correspondientes para cada una.
    P.ej. un diccionario donde:
      - key = URL
      - value = lista de clases a filtrar en esa URL
    """
    url_and_classes = {
        # URL 1 -> clases 1.1, 1.2, ...
        "https://www.prioritypass.com/": [
        # "banner-actions-container",
        # "banner-header",
        # "banner_logo",
        # "cookie-setting-link",
        # "default",
        # "ot-cookie-policy-link",
        # "ot-sdk-columns",
        # "ot-sdk-container",
        # "ot-sdk-row",
        # "ot-sdk-twelve",
        # "ot-wo-title",
        # "otCenterRounded",
        # "vertical-align-content",
        # "site-header__inner",
        # "site-footer", 
        # "cf",
        ],
        
        # URL 2 -> clases 2.1, 2.2, ...
        #"https://www.otro-sitio.com/": ["class-2.1", "class-2.2"]
        # Agrega tantas como necesites...
    }

    # Recorremos cada (URL, lista_clases) y lanzamos la función
    for url, classes in url_and_classes.items():
        await run_full_analysis(url, classes)

# =============================================================================
# 3) Punto de entrada
# =============================================================================

if __name__ == "__main__":
    asyncio.run(main())
