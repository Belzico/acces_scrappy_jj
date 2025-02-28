# main.py

import json
import asyncio
import os

from scraper.scraper import WebScraper
from accessibility_checker.axe_checker import analyze_accessibility, analyze_local_html
from reports.generate_report import generate_report

# Importamos el "tester global"
from manual_checks.global_tester import (
    run_all_testers,
    run_all_testers_in_folder,
    report_incidences_to_file
)

async def main():
    start_url = "https://www.joytoy.com"

    # Ejecutar el scraper (URLs en vivo)
    print("🔍 Scrapeando el sitio web...")
    scraper = WebScraper(start_url)
    pages = await scraper.run()

    # Ejecutar chequeo de accesibilidad con axe_core en las páginas vivas
    print("🧪 Analizando accesibilidad de las páginas vivas...")
    axe_results = []
    all_manual_incidences = []

    for page in pages:
        page_url = page["url"]
        print(f"Procesando página: {page_url}")

        # 1) Chequeo de accesibilidad con axe (URL real)
        accessibility_result = await analyze_accessibility(page_url)
        axe_results.append(accessibility_result)

        # 2) Chequeo manual de accesibilidad (testers globales)
        #    Nota: Esto asume que tu WebScraper ya guarda el HTML en page["content"].
        html_content = page.get("content", "")
        if not html_content:
            print(f"⚠️ No hay contenido HTML en {page_url} para pruebas manuales.")
            continue
        
        manual_incidences = run_all_testers(html_content, page_url)
        if manual_incidences:
            all_manual_incidences.extend(manual_incidences)
            report_incidences_to_file(manual_incidences, "manual_incidences.json")

    # Guardar los resultados de AXE en un JSON
    with open("accessibility_results.json", "w", encoding="utf-8") as f:
        json.dump(axe_results, f, indent=4, ensure_ascii=False)

    # Generar reporte global (de AXE, si así lo deseas)
    print("📊 Generando reporte de accesibilidad...")
    generate_report(axe_results)

    # ========== NUEVO: Analizar CARPETA local con archivos HTML ==========

    local_folder = "C:\\Users\\namic\\OneDrive\\Documentos\\GitHub\\acces_scrappy_jj\\html_samples"  # Ajusta la ruta a tu carpeta
    if os.path.isdir(local_folder):
        print(f"\n🗂  Analizando carpeta local: {local_folder}")

        # 1) Analizar accesibilidad con axe_core en cada archivo .html
        local_analysis_results = await analyze_local_html(local_folder)
        # Unimos estos resultados a los 'axe_results' si queremos un solo reporte
        axe_results.extend(local_analysis_results)

        # 2) Chequeo manual de accesibilidad para cada archivo .html
        #    usando la función 'run_all_testers_in_folder'.
        #    Esto hará la lectura del contenido y ejecutará testers manuales.
        folder_incidences = run_all_testers_in_folder(local_folder)
        if folder_incidences:
            # Guardamos también en el mismo 'manual_incidences.json'
            all_manual_incidences.extend(folder_incidences)
            report_incidences_to_file(folder_incidences, "manual_incidences.json")

    print("✅ Finalizado. Revisa 'accessibility_results.json' y 'manual_incidences.json'.")

if __name__ == "__main__":
    asyncio.run(main())
