import json
import asyncio
import os
from bs4 import BeautifulSoup

from scraper.scraper import WebScraper
from accessibility_checker.axe_checker import analyze_accessibility, analyze_local_html
from accessibility_checker.lighthouse_checker import analyze_lighthouse  # 🔥 NUEVO

from reports.generate_report import generate_report

from manual_checks.global_tester import (
    run_all_testers,
    run_all_testers_in_folder,
    report_incidences_to_file
)

FILTER_BY_CLASS = False  # Filtrar por clase específica
TARGET_CLASS = "web-inherited-reference"

async def main():
    start_url = "https://www.barcelo.com/en-us/"

    print("🔍 Scrapeando el sitio web...")
    scraper = WebScraper(start_url)
    pages = await scraper.run()

    print("🧪 Analizando accesibilidad de las páginas vivas...")
    axe_results = []
    lighthouse_errors = []  # 🔥 Guardamos aquí SOLO los errores de Lighthouse
    all_manual_incidences = []

    for page in pages:
        page_url = page["url"]
        print(f"Procesando página: {page_url}")

        # 1️⃣ Análisis con axe-core
        accessibility_result = await analyze_accessibility(page_url)
        axe_results.append(accessibility_result)

        # 2️⃣ Análisis con Lighthouse (solo errores)
        lighthouse_result = analyze_lighthouse(page_url)  # 🔥 NUEVO
        if lighthouse_result:
            lighthouse_errors.extend(lighthouse_result)  # Guardamos solo errores

        # 3️⃣ Chequeo manual
        html_content = page.get("content", "")
        if not html_content:
            print(f"⚠️ No hay contenido HTML en {page_url} para pruebas manuales.")
            continue

        if FILTER_BY_CLASS:
            soup = BeautifulSoup(html_content, "html.parser")
            target_elements = soup.find_all(class_=TARGET_CLASS)
            html_content = "".join(str(el) for el in target_elements)

            if not html_content.strip():
                print(f"⚠️ No se encontró la clase '{TARGET_CLASS}' en {page_url}. Omitiendo.")
                continue

        manual_incidences = run_all_testers(html_content, page_url)
        if manual_incidences:
            all_manual_incidences.extend(manual_incidences)
            report_incidences_to_file(manual_incidences, "manual_incidences.json")

    # Guardar resultados de AXE
    with open("accessibility_results.json", "w", encoding="utf-8") as f:
        json.dump(axe_results, f, indent=4, ensure_ascii=False)

    # Guardar SOLO ERRORES de Lighthouse en otro archivo
    with open("lighthouse_errors.json", "w", encoding="utf-8") as f:
        json.dump(lighthouse_errors, f, indent=4, ensure_ascii=False)

    print("📊 Generando reporte de accesibilidad...")
    generate_report(axe_results)

    # 📂 Analizar archivos locales
    local_folder = "C:\\Users\\namic\\OneDrive\\Documentos\\GitHub\\acces_scrappy_jj\\html_samples"
    if os.path.isdir(local_folder):
        print(f"\n🗂  Analizando carpeta local: {local_folder}")

        local_analysis_results = await analyze_local_html(local_folder)
        axe_results.extend(local_analysis_results)

        folder_incidences = []
        for file_name in os.listdir(local_folder):
            if file_name.endswith(".html"):
                file_path = os.path.join(local_folder, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if FILTER_BY_CLASS:
                    soup = BeautifulSoup(content, "html.parser")
                    target_elements = soup.find_all(class_=TARGET_CLASS)
                    content = "".join(str(el) for el in target_elements)

                    if not content.strip():
                        print(f"⚠️ No se encontró la clase '{TARGET_CLASS}' en {file_name}. Omitiendo.")
                        continue

                incidences = run_all_testers(content, file_path)
                folder_incidences.extend(incidences)

        if folder_incidences:
            all_manual_incidences.extend(folder_incidences)
            report_incidences_to_file(folder_incidences, "manual_incidences.json")

    print("✅ Finalizado. Revisa 'accessibility_results.json', 'lighthouse_errors.json' y 'manual_incidences.json'.")

if __name__ == "__main__":
    asyncio.run(main())
