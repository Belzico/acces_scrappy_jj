✅ WCAG 1.4.11 - Contraste de Componentes Interactivos (Dropdown Focused/Selected)
Este script en Python analiza el contenido HTML de un sitio web para verificar si las opciones de un menú desplegable (<select>) en estado activo, enfocado o seleccionado, cumplen con la relación de contraste mínima establecida por el criterio WCAG 2.2 - Criterio 1.4.11: Contraste de Componentes No Textuales.

🧪 Objetivo
Detectar fallos de contraste cuando:

La opción seleccionada (selected) o enfocada de un <select> no alcanza la relación mínima de contraste 3:1 entre el texto y el fondo.

El usuario no puede identificar visualmente qué opción está activa o en foco por falta de contraste suficiente.

📦 Funciones incluidas
Función	Descripción
run_all___1_4_11	Verifica el contraste entre el texto y fondo de opciones <option> en estado :selected o :focus. Extrae estilos desde bloques CSS embebidos y calcula la relación de contraste.
🧰 Uso de la función principal
python
Copy
Edit
from check__1_4_11 import run_all___1_4_11

issues = run_all___1_4_11(html_content, page_url)
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

transform_json_to_excel.py (módulo personalizado de exportación)

📚 Referencia
WCAG 2.2 - Criterio 1.4.11: Contraste de Componentes No Textuales

Guía oficial de contraste para elementos interactivos (WAI)