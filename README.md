# 🚀 Web Accessibility Analyzer

Este proyecto realiza un **análisis automático y manual de accesibilidad web** utilizando Pyppeteer, axe-core, Lighthouse y una serie de pruebas manuales adicionales. Detecta errores de accesibilidad y genera reportes detallados para mejorar la conformidad con WCAG 2.2.

## 📜 Índice
1. [📌 Introducción](#-introducción)
2. [🔧 Instalación](#-instalación)
3. [🖥️ Uso](#️-uso)
4. [📂 Estructura del Proyecto](#-estructura-del-proyecto)
5. [🔍 Scraper](#-scraper)
6. [🧪 Axe Checker](#-axe-checker)
7. [🚦 Lighthouse Analyzer](#-lighthouse-analyzer)
8. [🛠️ Global Tester](#-global-tester)
9. [📖 Documentación de Testers](#-documentación-de-testers)
10. [📚 Referencias](#-referencias)

---

## 📌 Introducción
Este proyecto permite **analizar la accesibilidad de páginas web** mediante un **scraper**, pruebas automáticas con **axe-core** y **Lighthouse**, además de validaciones manuales mediante **testers personalizados**.

Se generan reportes detallados con **incidencias detectadas y soluciones recomendadas**.

---

## 🔧 Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
Instala las dependencias:

sh
Copy
Edit
pip install -r requirements.txt
Copia la carpeta chrome-win en la raíz del proyecto (necesario para Pyppeteer).

Si no tienes chrome-win, descárgalo y colócalo en la carpeta del proyecto.
Configura tu API Key de OpenAI para análisis semántico (opcional):

sh
Copy
Edit
export OPENAI_API_KEY="tu-clave-api"
🖥️ Uso
Para ejecutar el análisis de accesibilidad en una página web:

sh
Copy
Edit
python main.py
Para analizar archivos locales dentro de la carpeta html_samples:

sh
Copy
Edit
python main.py --local html_samples
📂 Estructura del Proyecto
bash
Copy
Edit
📁 acces_scrappy_jj
│── 📁 accessibility_checker    # Análisis de accesibilidad con axe-core y Lighthouse
│── 📁 scraper                 # Scraper para extraer HTML de URLs
│── 📁 manual_checks           # Testers manuales de accesibilidad
│── 📁 reports                 # Generación de reportes
│── 📁 chrome-win              # Binario de Chromium necesario para Pyppeteer
│── main.py                    # Punto de entrada del proyecto
│── requirements.txt            # Dependencias del proyecto
│── README.md                   # Documentación
🔍 Scraper
Ubicado en scraper/scraper.py, este módulo extrae contenido HTML de páginas web utilizando Pyppeteer.

Utiliza un navegador sin interfaz (headless) para cargar la página.
Espera hasta que el DOM esté completamente cargado.
Extrae el contenido HTML para su posterior análisis.
🧪 Axe Checker
Ubicado en accessibility_checker/axe_checker.py, este módulo ejecuta pruebas automáticas de accesibilidad con axe-core.

Inyecta axe-core en la página cargada con Pyppeteer.
Ejecuta axe.run() para detectar violaciones WCAG.
Guarda los resultados en accessibility_results.json.
📌 Referencia oficial: Axe-Core Docs

🚦 Lighthouse Analyzer
Ubicado en accessibility_checker/lighthouse_checker.py, este módulo ejecuta auditorías de accesibilidad usando Google Lighthouse.

Analiza accesibilidad, rendimiento y SEO.
Extrae solo los errores detectados para su análisis.
Guarda los resultados en lighthouse_errors.json.
📌 Referencia oficial: Lighthouse Docs

🛠️ Global Tester
Ubicado en manual_checks/global_tester.py, este módulo ejecuta pruebas manuales personalizadas.

Carga y ejecuta testers definidos en manual_checks/.
Guarda los errores detectados en manual_incidences.json.
📌 Cómo agregar un nuevo tester:

Crea un archivo en manual_checks/, por ejemplo: check_new_test.py.
Define una función que reciba html_content y page_url y retorne una lista de incidencias.
Agrega tu tester a la lista en global_tester.py.
Ejemplo de un tester:

python
Copy
Edit
from bs4 import BeautifulSoup

def check_missing_alt(html_content, page_url):
    """Detecta imágenes sin atributo 'alt'."""
    soup = BeautifulSoup(html_content, "html.parser")
    incidences = []
    for img in soup.find_all("img"):
        if not img.get("alt"):
            incidences.append({
                "title": "Image missing alt attribute",
                "page_url": page_url,
                "element": str(img),
                "description": "This image lacks an alternative text description.",
                "remediation": "Add a meaningful alt attribute."
            })
    return incidences
📖 Documentación de Testers
Cada tester detecta problemas específicos y sigue las reglas WCAG:

Tester	Descripción	WCAG
check_alt_distinction.py	Detecta imágenes sin alt o con alt redundante	1.1.1
check_images_decorative.py	Detecta imágenes decorativas mal configuradas	1.1.1
check_links_with_no_text.py	Detecta enlaces/botones sin texto accesible	2.4.4
check_keyboard_accessibility.py	Detecta elementos sin soporte para teclado	2.1.1
check_focus_visible.py	Detecta elementos sin indicador de foco visible	2.4.7
📌 Referencias oficiales:

Guía de imágenes decorativas (W3C)
Pautas WCAG 2.1
📚 Referencias
🏗 Pyppeteer: https://github.com/pyppeteer/pyppeteer
🏗 Axe-Core: https://github.com/dequelabs/axe-core
🏗 Lighthouse: https://developers.google.com/web/tools/lighthouse
🏗 WCAG 2.1: https://www.w3.org/TR/WCAG21/
🏗 Sentence Transformers: https://www.sbert.net/
🏗 OpenAI Embeddings: https://platform.openai.com/docs/guides/embeddings
📢 ¡Contribuye! Si encuentras errores o quieres mejorar la herramienta, envía un Pull Request o abre un Issue en el repositorio. 🚀