import asyncio
import os
import requests
from pyppeteer import launch
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

CHROMIUM_PATH = "./chrome-win/chrome.exe"

class WebScraper:
    def __init__(self, start_url, max_pages=1, max_depth=2):
        self.start_url = start_url
        self.visited_urls = {}
        self.page_count = 0  # Contador de páginas visitadas correctamente
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.browser = None  # Aquí guardaremos el navegador

        # Carpeta donde guardamos las imágenes
        self.images_folder = "downloaded_images"
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)

    async def scrape_page(self, url, depth=0):
        """Scrapea una página y busca enlaces internos recursivamente."""
        # Si ya alcanzamos el límite de páginas, no seguir
        if self.page_count >= self.max_pages:
            return []

        # Normalizar la URL (sin querystring ni fragment)
        parsed_url = urlparse(url)
        normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        # Verificar si ya visitamos la página o si pasamos la profundidad
        if normalized_url in self.visited_urls or depth > self.max_depth:
            return []

        # Marcar en visited_urls para no reintentar
        self.visited_urls[normalized_url] = True

        # Crear una nueva pestaña (no un nuevo navegador)
        page = await self.browser.newPage()

        loaded_correctly = False
        for attempt in range(3):
            try:
                print(f"Intento {attempt+1}/3 de cargar: {normalized_url}")
                await page.goto(url, {"waitUntil": "domcontentloaded", "timeout": 60000})
                loaded_correctly = True
                break
            except Exception as e:
                print(f"⚠️ Intento {attempt+1} fallido en {normalized_url}: {e}")

        if not loaded_correctly:
            print(f"❌ No se pudo cargar {normalized_url}. Omitiendo...\n")
            await page.close()
            return []

        # Si cargó correctamente, extraemos el contenido HTML
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        # Cerramos la pestaña
        await page.close()

        # Ahora sí sumamos 1 a nuestro contador
        self.page_count += 1
        print(f"Scrapeando ({self.page_count}/{self.max_pages}): {normalized_url}\n")

        # ─────────────────────────────────────────────────────────────
        # NUEVO: Descarga de imágenes encontradas en la página actual
        local_images = self.download_images(soup, base_url=normalized_url)
        # ─────────────────────────────────────────────────────────────

        # Extraer enlaces internos
        links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
        # Filtrar sólo aquellos que comienzan con self.start_url, así evitamos salir de dominio
        links = list(set(filter(lambda x: x.startswith(self.start_url), links)))

        # Recolectamos la info del "page actual"
        page_results = [{
            "url": normalized_url,
            "content": content,
            "local_images": local_images  # Rutas locales de las imágenes descargadas
        }]

        # Recorrer recursivamente los enlaces (mientras no se supere el límite)
        for link in links:
            if self.page_count < self.max_pages:
                child_pages = await self.scrape_page(link, depth+1)
                page_results.extend(child_pages)
            else:
                break

        return page_results

    def download_images(self, soup, base_url):
        """
        Busca <img> en 'soup' y descarga cada imagen en self.images_folder.
        Retorna una lista con las rutas locales de las imágenes descargadas.
        """
        local_paths = []

        images = soup.find_all("img")
        for img in images:
            src = img.get("src")
            if not src:
                continue

            # Resolver URL relativa con respecto a la página base
            image_url = urljoin(base_url, src)

            try:
                response = requests.get(image_url, stream=True, timeout=10)
                if response.status_code == 200:
                    # Nombre de archivo basado en la parte final de la URL
                    filename = os.path.basename(urlparse(image_url).path)
                    if not filename:
                        # Si la URL termina en '/', asignar un nombre genérico
                        filename = "image.jpg"

                    local_path = os.path.join(self.images_folder, filename)

                    # Evita sobreescribir si ya existe (puedes usar otro método si lo deseas)
                    # Aquí se sobreescribe si el nombre coincide
                    with open(local_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            f.write(chunk)

                    local_paths.append(local_path)
            except Exception as e:
                print(f"⚠️ Error descargando {image_url}: {e}")

        return local_paths

    async def run(self):
        """
        Inicia el navegador (headless) y arranca el scraping a partir de self.start_url.
        Retorna una lista de diccionarios con la información de cada página scrapeada:
        {
          "url": <URL de la página>,
          "content": <HTML raw>,
          "local_images": [<ruta local img1>, <ruta local img2>, ...]
        }
        """
        self.browser = await launch(
            headless=True,
            executablePath=CHROMIUM_PATH,
            args=["--no-sandbox"]
        )

        results = await self.scrape_page(self.start_url)

        # Cierra el navegador al terminar
        await self.browser.close()

        return results

