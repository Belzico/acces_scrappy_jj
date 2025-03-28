
✅ WCAG 2.4.3 - Orden del Foco (Focus Order)
Este script automatizado en Python analiza el contenido HTML para detectar problemas relacionados con el orden del foco, cumpliendo con el criterio WCAG 2.2 - Criterio 2.4.3: Orden del Foco.

🧪 Objetivo
Detectar errores relacionados con:

Uso incorrecto del atributo tabindex (por ejemplo, valores mayores que 0 o -1 en elementos interactivos).

Elementos interactivos (como enlaces) que no son alcanzables mediante navegación con teclado.

Diálogos modales (<dialog>) que no tienen el atributo open, lo cual puede interferir con la gestión del foco.

📦 Checkers incluidos
Este archivo audita patrones que pueden romper el flujo natural del foco en la interfaz:

Función	Descripción
run_all___2_4_3	Evalúa problemas relacionados con el atributo tabindex, enlaces sin href, y modales sin atributo open.
🧰 Uso de la función general
python
Copy
Edit
from check__2_4_3 import run_all___2_4_3

issues = run_all___2_4_3(html_content, page_url)
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
WCAG 2.2 - Criterio 2.4.3: Orden del Foco

WAI - Accesibilidad en la navegación por teclado

