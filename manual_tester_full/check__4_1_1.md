✅ WCAG 4.1.1 - Verificación de Estructura HTML: IDs Únicos y Jerarquía de Listas
Este script automatizado en Python analiza el contenido HTML para detectar problemas estructurales que afectan la accesibilidad y el funcionamiento correcto de tecnologías de asistencia, de acuerdo con el criterio WCAG 2.2 - Criterio 4.1.1: Procesamiento.

🧪 Objetivo
Detectar errores relacionados con:

Atributos id duplicados en el DOM, que pueden romper funcionalidades de scripts y lectores de pantalla.

Elementos <div> usados incorrectamente como hijos directos de listas <ul> o <ol>, lo que rompe la semántica del HTML.

📦 Checkers incluidos
Este archivo agrupa múltiples validaciones relacionadas con la estructura y parsing del documento:

Función	Descripción
run_all___4_1_1	Ejecuta todas las validaciones asociadas al criterio 4.1.1 (estructura HTML válida).
🔎 Validaciones realizadas
🔁 ID duplicado: Se detectan atributos id usados más de una vez en el documento.

📦 Estructura de listas: Se identifican elementos <div> colocados directamente dentro de listas <ul> o <ol>, violando la semántica permitida (solo <li>, <script> o <template> son válidos).

🧰 Uso de la función general
python
Copy
Edit
from check__4_1_1 import run_all___4_1_1

issues = run_all___4_1_1(html_content, page_url)
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
WCAG 2.2 - Criterio 4.1.1: Procesamiento

Guías oficiales sobre estructura semántica del contenido web (WAI)

