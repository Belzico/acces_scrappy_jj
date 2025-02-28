import asyncio
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

    async def scrape_page(self, url, depth=0):
        """Scrapea una página y busca enlaces internos recursivamente"""

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

        # Si cargó correctamente, extraemos el contenido
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        # Cerramos la pestaña
        await page.close()

        # Ahora sí sumamos 1 a nuestro contador y mostramos el mensaje
        self.page_count += 1
        print(f"Scrapeando ({self.page_count}/{self.max_pages}): {normalized_url}\n")

        # Extraer enlaces internos
        links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
        # Filtrar sólo aquellos que comienzan con self.start_url, así evitamos salir de dominio
        links = list(set(filter(lambda x: x.startswith(self.start_url), links)))

        # Recorrer recursivamente los enlaces (mientras no se supere el límite)
        for link in links:
            if self.page_count < self.max_pages:
                await self.scrape_page(link, depth+1)
            else:
                break

        # Devolvemos la info de la página actual
        return [{"url": normalized_url, "content": content}]

    async def run(self):
        # Abre el navegador UNA sola vez
        self.browser = await launch(
            headless=True,
            executablePath=CHROMIUM_PATH,
            args=["--no-sandbox"]
        )

        # Inicia el scraping desde la URL base
        results = await self.scrape_page(self.start_url)

        # Cierra el navegador al terminar
        await self.browser.close()

        return results

if __name__ == "__main__":
    start_url = "https://www.joytoy.com"
    scraper = WebScraper(start_url, max_pages=5)
    loop = asyncio.get_event_loop()
    pages = loop.run_until_complete(scraper.run())
    print(f"✅ Scraping completado. Se extrajeron {len(pages)} páginas correctamente.")
