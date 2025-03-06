# 🚀 Proyecto de Accesibilidad Web

Este proyecto realiza un **análisis automático y manual de accesibilidad web** utilizando Pyppeteer, axe-core y un conjunto de pruebas manuales adicionales. Se enfoca en detectar errores comunes de accesibilidad y generar reportes detallados.

## 📜 Índice
1. [📌 Introducción](#-introducción)
2. [🔧 Instalación](#-instalación)
3. [🖥️ Uso](#️-uso)
4. [📂 Estructura del Proyecto](#-estructura-del-proyecto)
5. [🔍 Scraper](#-scraper)
6. [🧪 Axe Checker](#-axe-checker)
7. [🛠️ Global Tester](#-global-tester)
8. [📖 Documentación de Testers](#-documentación-de-testers)
9. [📚 Referencias](#-referencias)

---

## 📌 Introducción
Este proyecto permite analizar la accesibilidad de páginas web extrayendo su contenido con un **scraper**, ejecutando pruebas automáticas con **axe-core** y validaciones manuales a través de un conjunto de **testers personalizados**.

Se generan reportes detallados sobre los problemas detectados y cómo solucionarlos.

---

## 🔧 Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```
2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
3. **Copia la carpeta `chrome-win` en la raíz del proyecto.**
   - Pyppeteer necesita un binario de Chromium para ejecutarse.
   - Si no tienes `chrome-win`, descárgalo y colócalo en la carpeta del proyecto.

4. Configura tu API Key de OpenAI para análisis semántico (opcional):
   ```sh
   export OPENAI_API_KEY="tu-clave-api"
   ```

---

## 🖥️ Uso
Para ejecutar el análisis de accesibilidad en una página web:
```sh
python main.py
```
Para analizar archivos locales dentro de la carpeta `html_samples`:
```sh
python main.py --local html_samples
```

---

## 📂 Estructura del Proyecto
```
📁 acces_scrappy_jj
│── 📁 accessibility_checker    # Analiza accesibilidad con axe-core
│── 📁 scraper                 # Scraper para extraer HTML de URLs
│── 📁 manual_checks           # Testers manuales de accesibilidad
│── 📁 reports                 # Generación de reportes
│── 📁 chrome-win              # Binario de Chromium necesario para Pyppeteer
│── main.py                    # Punto de entrada del proyecto
│── requirements.txt            # Dependencias del proyecto
│── README.md                   # Documentación
```

---

## 🔍 Scraper
Ubicado en `scraper/scraper.py`, este módulo **extrae contenido HTML de páginas web** utilizando **Pyppeteer**. 

- Utiliza un navegador sin interfaz (`headless`) para cargar la página.
- Espera hasta que el DOM esté completamente cargado.
- Extrae el contenido HTML para su posterior análisis.

---

## 🧪 Axe Checker
Ubicado en `accessibility_checker/axe_checker.py`, este módulo **ejecuta pruebas automáticas de accesibilidad** usando la librería **axe-core**.

- Inyecta `axe-core` en la página cargada con Pyppeteer.
- Ejecuta `axe.run()` para obtener un reporte de violaciones WCAG.
- Guarda los resultados en `accessibility_results.json`.

📌 **Referencia oficial:** [Axe-Core Docs](https://dequeuniversity.com/rules/axe)

---

## 🛠️ Global Tester
Ubicado en `manual_checks/global_tester.py`, este módulo **ejecuta pruebas manuales personalizadas**.

- **Carga todos los testers definidos en `manual_checks/`**.
- **Ejecuta cada tester sobre el contenido HTML** de la página.
- **Guarda los errores detectados en `manual_incidences.json`**.

📌 **Cómo agregar un nuevo tester:**
1. Crea un archivo en `manual_checks/`, por ejemplo: `check_new_test.py`.
2. Define una función que reciba `html_content` y `page_url` y retorne una lista de incidencias.
3. Agrega tu nuevo tester a la lista en `global_tester.py`.

Ejemplo de un tester:
```python
from bs4 import BeautifulSoup

def check_missing_alt(html_content, page_url):
    """Detecta imágenes sin atributo 'alt'."""
    soup = BeautifulSoup(html_content, "html.parser")
    incidencias = []
    for img in soup.find_all("img"):
        if not img.get("alt"):
            incidencias.append({
                "title": "Imagen sin alt",
                "page": page_url,
                "element": str(img),
                "description": "Esta imagen no tiene un texto alternativo.",
                "suggested_fix": "Agregar un alt descriptivo."
            })
    return incidencias
```

---

## 📖 Documentación de Testers

Cada tester detecta problemas específicos y sigue las reglas WCAG:

| Tester | Descripción | WCAG |
|--------|------------|------|
| `check_alt_distinction.py` | Detecta imágenes sin `alt` o con `alt` redundante | 1.1.1 |
| `check_images_decorative.py` | Detecta imágenes decorativas mal configuradas | 1.1.1 |
| `check_links_with_no_text.py` | Detecta enlaces/botones sin texto accesible | 2.4.4 |

📌 **Referencias oficiales:**
- [Guía de imágenes decorativas (W3C)](https://www.w3.org/WAI/tutorials/images/decorative/)
- [Pautas WCAG 2.1](https://www.w3.org/TR/WCAG21/)

---

## 📚 Referencias

- 🏗 **Pyppeteer**: [https://github.com/pyppeteer/pyppeteer](https://github.com/pyppeteer/pyppeteer)
- 🏗 **Axe-Core**: [https://github.com/dequelabs/axe-core](https://github.com/dequelabs/axe-core)
- 🏗 **WCAG 2.1**: [https://www.w3.org/TR/WCAG21/](https://www.w3.org/TR/WCAG21/)
- 🏗 **Sentence Transformers**: [https://www.sbert.net/](https://www.sbert.net/)
- 🏗 **OpenAI Embeddings**: [https://platform.openai.com/docs/guides/embeddings](https://platform.openai.com/docs/guides/embeddings)

---

📢 **¡Contribuye!**
Si encuentras errores o quieres mejorar la herramienta, envía un **Pull Request** o abre un **Issue** en el repositorio. 🚀

