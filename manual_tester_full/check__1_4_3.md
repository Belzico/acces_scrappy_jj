✅ WCAG 1.4.3 - Verificación de Contraste en Dropdowns y Placeholders
Este script automatizado en Python analiza contenido HTML para detectar problemas de contraste visual entre texto y fondo en campos de formulario, cumpliendo con el criterio WCAG 2.2 - Criterio 1.4.3: Contraste (mínimo).

🧪 Objetivo
Detectar errores relacionados con:

Opciones seleccionadas en dropdowns (<select>) que no cumplen con la relación mínima de contraste 4.5:1 entre el texto y el fondo.

Texto de placeholder en campos <input> con color gris claro u otros valores que no contrastan adecuadamente con el fondo blanco o claro.

📦 Checkers incluidos
Este archivo agrupa múltiples funciones que auditan distintos patrones de contraste de texto en interfaces gráficas:

Función	Descripción
check_dropdown_contrast	Evalúa si la opción seleccionada en un <select> cumple con el contraste mínimo (4.5:1).
check_placeholder_contrast	Evalúa si el texto del placeholder tiene suficiente contraste con el fondo.
🧰 Uso de la función general
python
Copy
Edit
from check__1_4_3 import run_all___1_4_3

issues = run_all___1_4_3(html_content, page_url)
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
WCAG 2.2 - Criterio 1.4.3: Contraste (mínimo)

Guía sobre contraste mínimo del contenido no textual (WAI)

¿Te gustaría que prepare un README combinado que resuma todos los checkers WCAG implementados en tu suite hasta ahora?