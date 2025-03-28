✅ WCAG 1.4.1 - Uso del Color: Verificador de Enlaces y Botones
Este script automatizado en Python analiza el contenido HTML para verificar que los elementos interactivos no dependan únicamente del color para transmitir información, de acuerdo con el criterio WCAG 2.2 - Criterio 1.4.1: Uso del color.

🧪 Objetivo
Detectar errores relacionados con:

Enlaces o botones que no tienen indicios visuales suficientes aparte del color (por ejemplo, sin subrayado, borde o fondo).

Elementos interactivos que podrían no ser reconocidos como tales por personas con discapacidad visual o daltonismo.

📦 Checker incluido
Este archivo ejecuta un verificador para evaluar la accesibilidad visual de botones y enlaces:

Función	Descripción
run_all___1_4_1	Identifica botones o enlaces que podrían depender únicamente del color para ser reconocidos.
🧰 Uso de la función general
python
Copy
Edit
from check__1_4_1 import run_all___1_4_1

issues = run_all___1_4_1(html_content, page_url)
El archivo Excel generado incluirá una fila por cada incidencia detectada.

Si no se detectan errores, se incluirá una fila con una justificación positiva:
"Justificación de los CPs asignados que no generen issues".

📤 Formato de salida
El reporte Excel incluye las siguientes columnas:

Title

Steps

Bug Type

Priority

Expected Result

Actual Result

Suggested resolution(s)

Failed checkpoint

User Impact

(+ Justification si no hay errores)

📌 Requisitos
Python 3.8+

Librerías necesarias:
beautifulsoup4

openpyxl (usada por transform_json_to_excel)

transform_json_to_excel (módulo personalizado de exportación)

📚 Referencia
WCAG 2.2 - Criterio 1.4.1: Uso del color

Guía sobre buenas prácticas de accesibilidad visual y diseño inclusivo (WAI)