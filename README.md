🚀 Web Accessibility Analyzer
Este proyecto realiza un análisis automático y manual de accesibilidad web utilizando Pyppeteer, axe-core, Lighthouse y una serie de testers personalizados alineados con WCAG 2.2.
Detecta errores de accesibilidad, justifica los CPs sin incidencias y genera reportes completos en JSON y Excel.

📜 Índice
📌 Introducción

🔧 Instalación

🖥️ Uso

📂 Estructura del Proyecto

🔍 Scraper

🧪 Axe Checker

🚦 Lighthouse Analyzer

🛠️ Global Tester (Manual Checks)

📖 Documentación de Testers

📊 Reportes Generados

📚 Referencias

🤝 Contribuye

📌 Introducción
Este sistema permite analizar páginas web y archivos HTML locales en busca de errores de accesibilidad.
Utiliza herramientas automáticas (axe-core, Lighthouse), un scraper personalizado, y una batería de testers manuales agrupados por criterios WCAG.

Los resultados se exportan en formatos estandarizados.
🔹 Si no se detectan incidencias, se documenta una justificación por CP.

🔧 Instalación
Clona el repositorio:

bash
Copy
Edit
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
Instala las dependencias:

bash
Copy
Edit
pip install -r requirements.txt
Copia la carpeta chrome-win en la raíz del proyecto.

⚠️ Este paso es obligatorio para que Pyppeteer funcione correctamente.
Si no tienes la carpeta, descárgala desde este enlace oficial de Chromium o desde una instalación existente.

(Opcional) Configura tu API Key de OpenAI para análisis semántico:

bash
Copy
Edit
export OPENAI_API_KEY="tu-clave-api"
🖥️ Uso
Para analizar una URL:

bash
Copy
Edit
python main.py
Para analizar archivos locales:

bash
Copy
Edit
python main.py --local html_samples
📂 Estructura del Proyecto
bash
Copy
Edit
📁 acces_scrappy_jj
├── 📁 accessibility_checker     # axe-core y Lighthouse
├── 📁 scraper                   # Extracción de HTML con Pyppeteer
├── 📁 manual_checks             # Testers manuales organizados por criterios WCAG
├── 📁 reports                   # Reportes generados (JSON + Excel)
├── 📁 chrome-win                # Chromium portátil para Pyppeteer
├── main.py                     # Script principal
├── requirements.txt            # Dependencias
└── README.md                   # Este archivo
🔍 Scraper
Ubicado en scraper/scraper.py, permite navegar páginas web y extraer su contenido HTML:

Usa Pyppeteer (modo headless).

Espera a la carga completa del DOM.

Retorna el HTML para su análisis.

🧪 Axe Checker
Ubicado en accessibility_checker/axe_checker.py:

Inyecta axe-core en la página cargada.

Ejecuta axe.run() y detecta violaciones WCAG.

Exporta los resultados a accessibility_results.json.

📌 Referencia: Axe-Core Docs

🚦 Lighthouse Analyzer
Ubicado en accessibility_checker/lighthouse_checker.py:

Ejecuta auditoría con Google Lighthouse.

Filtra las incidencias de accesibilidad.

Exporta a lighthouse_errors.json.

📌 Referencia: Lighthouse Docs

🛠️ Global Tester (Manual Checks)
Ubicado en manual_checks/global_tester.py:

Ejecuta todos los testers definidos por criterios WCAG.

Genera resultados en manual_incidences.json.

Si no hay incidencias, justifica con:

perl
Copy
Edit
Justificación de los CPs asignados que no generen issues
📌 Puedes añadir nuevos testers dentro de manual_checks/ según el criterio WCAG correspondiente.

📖 Documentación de Testers
Tester	Descripción	WCAG
testers_1_1_1.py	Imágenes sin alt, decorativas mal configuradas	1.1.1
testers_1_4_3.py	Contraste de texto (placeholders y dropdowns)	1.4.3
testers_1_4_4.py	Texto que se corta al hacer zoom al 200%	1.4.4
testers_1_4_5.py	Imágenes con texto no equivalente (OCR)	1.4.5
testers_1_4_10.py	Problemas de reflow a 320px (scroll horizontal, fixed width)	1.4.10
testers_1_4_11.py	Contraste de opciones seleccionadas en dropdown	1.4.11
testers_1_4_12.py	Recorte de contenido por espacio de texto (text spacing)	1.4.12
testers_2_1_1.py	Interacciones con mouse sin soporte de teclado	2.1.1
testers_2_4_3.py	Orden de foco incorrecto (tabindex, modales sin open, etc.)	2.4.3
testers_2_4_4.py	Enlaces y botones sin texto accesible	2.4.4
testers_2_4_7.py	Indicadores de foco visibles ausentes	2.4.7
testers_3_3_1.py	Formularios sin mensajes de error visibles	3.3.1
testers_4_1_1.py	IDs duplicados y estructuras HTML mal anidadas	4.1.1
testers_4_1_2.py	Name, Role y Value de elementos interactivos	4.1.2
📊 Reportes Generados
Archivo	Contenido
accessibility_results.json	Resultado del análisis con axe-core
lighthouse_errors.json	Errores de Lighthouse (accesibilidad únicamente)
manual_incidences.json	Incidencias detectadas por testers manuales
report.xlsx	Reporte consolidado (incluye justificaciones si no hay errores)
📚 Referencias
🧪 Pyppeteer

🧪 Axe-Core

🧪 Lighthouse

📘 WCAG 2.2

🧠 Sentence Transformers

🧠 OpenAI Embeddings

🤝 Contribuye
¿Tienes ideas, encontraste un bug o quieres colaborar?
¡Envíanos un Pull Request o abre un Issue! 💬🚀