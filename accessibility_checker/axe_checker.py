import asyncio
import json
import os
from pyppeteer import launch

CHROMIUM_PATH = "./chrome-win/chrome.exe"
AXE_JS_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.4.1/axe.min.js"


async def analyze_local_html(folder_path):
    """
    Ejecuta axe-core en todos los archivos .html dentro de la carpeta 'folder_path'.
    """

    # 1️⃣ Verificar que la ruta es una carpeta válida
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"🚫 La ruta {folder_path} no es una carpeta válida.")

    # 2️⃣ Obtener lista de archivos .html en la carpeta
    html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]
    if not html_files:
        print(f"⚠️ No se encontraron archivos .html en {folder_path}.")
        return []

    # 3️⃣ Abrir navegador UNA sola vez para procesar todos los archivos
    browser = await launch(headless=True, executablePath=CHROMIUM_PATH, args=["--no-sandbox"])
    results = []

    try:
        for html_file in html_files:
            file_path = os.path.join(folder_path, html_file)  # Ruta completa del archivo
            abs_path = os.path.abspath(file_path)
            file_url = "file:///" + abs_path.replace("\\", "/")  # Convertir a URL local

            page = await browser.newPage()

            try:
                # 4️⃣ Cargar el archivo HTML local en el navegador
                await page.goto(file_url, {"waitUntil": "domcontentloaded", "timeout": 60000})

                # 5️⃣ Inyectar axe-core en la página
                await page.addScriptTag({"url": AXE_JS_URL})
                await asyncio.sleep(2)

                # 6️⃣ Verificar si axe-core se cargó antes de ejecutarlo
                axe_loaded = await page.evaluate("typeof axe !== 'undefined'")
                if not axe_loaded:
                    raise RuntimeError("axe-core no se cargó correctamente")

                # 7️⃣ Ejecutar análisis de accesibilidad con axe
                axe_result = await page.evaluate("axe.run()")
                results.append({
                    "file_path": file_path,
                    "violations": axe_result.get("violations", [])
                })

            except Exception as e:
                print(f"❌ Error al analizar {file_path}: {e}")
                results.append({
                    "file_path": file_path,
                    "violations": [],
                    "error": str(e)
                })

            finally:
                await page.close()  # Cerramos la pestaña

    finally:
        await browser.close()  # Cerramos el navegador

    return results


async def analyze_accessibility(url):
    """
    Ejecuta axe-core en una página con Chromium usando una URL online.
    (Código original tuyo, mantenemos la lógica, solo añadimos comentarios)
    """
    browser = await launch(headless=True, executablePath=CHROMIUM_PATH, args=["--no-sandbox"])
    page = await browser.newPage()

    try:
        await page.goto(url, {"waitUntil": "domcontentloaded", "timeout": 60000})

        # Inyectar axe-core correctamente
        await page.addScriptTag({"url": AXE_JS_URL})

        # Esperar un poco para asegurarnos de que axe-core está disponible
        await asyncio.sleep(2)

        # Verificar si axe-core se cargó antes de ejecutarlo
        axe_loaded = await page.evaluate("typeof axe !== 'undefined'")
        if not axe_loaded:
            raise RuntimeError("axe-core no se cargó correctamente")

        # Ejecutar análisis con axe-core
        results = await page.evaluate("axe.run()")
        return {"url": url, "violations": results.get("violations", [])}

    except Exception as e:
        print(f"❌ Error al analizar {url}: {e}")
        return {"url": url, "violations": [], "error": str(e)}

    finally:
        # Asegurar que el navegador se cierre incluso si ocurre un error
        await browser.close()


async def analyze_local_html(folder_path):
    """
    Ejecuta axe-core en todos los archivos .html dentro de la carpeta 'folder_path'.

    1) Verifica que 'folder_path' sea una carpeta.
    2) Busca todos los .html y los analiza con Pyppeteer + axe (igual que antes, pero para cada archivo).
    3) Retorna una lista de resultados, uno por cada archivo analizado.
    """

    # 1) Verificar que sea una carpeta válida
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"La ruta {folder_path} no es una carpeta válida.")

    # Obtenemos la lista de archivos .html
    html_files = [f for f in os.listdir(folder_path) if f.endswith(".html")]
    if not html_files:
        print(f"⚠️ No se encontraron archivos .html en {folder_path}")
        return []

    # Lanzamos el navegador UNA sola vez, luego abrimos/cerramos páginas para cada archivo
    browser = await launch(headless=True, executablePath=CHROMIUM_PATH, args=["--no-sandbox"])
    results = []

    try:
        for html_file in html_files:
            file_path = os.path.join(folder_path, html_file)
            abs_path = os.path.abspath(file_path)
            file_url = "file:///" + abs_path.replace("\\", "/")

            page = await browser.newPage()
            try:
                # Cargamos cada archivo local
                await page.goto(file_url, {"waitUntil": "domcontentloaded", "timeout": 60000})

                # Inyectar axe-core
                await page.addScriptTag({"url": AXE_JS_URL})
                await asyncio.sleep(2)

                # Verificar si axe-core está disponible
                axe_loaded = await page.evaluate("typeof axe !== 'undefined'")
                if not axe_loaded:
                    raise RuntimeError("axe-core no se cargó correctamente")

                # Ejecutamos axe.run()
                axe_result = await page.evaluate("axe.run()")
                results.append({
                    "file_path": file_path,
                    "violations": axe_result.get("violations", [])
                })

            except Exception as e:
                print(f"❌ Error al analizar {file_path}: {e}")
                results.append({
                    "file_path": file_path,
                    "violations": [],
                    "error": str(e)
                })

            finally:
                # Cerramos la pestaña (no el navegador completo)
                await page.close()

    finally:
        # Al terminar todos los archivos, cerramos el navegador
        await browser.close()

    return results



