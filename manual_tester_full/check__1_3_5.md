✅ WCAG 1.3.5 - Identificar Propósito del Campo de Entrada: Verificador de Autocompletado en Formularios

Este script automatizado en Python analiza el contenido HTML para verificar que los campos de formulario que recopilan información personal del usuario incluyan el atributo `autocomplete` con un valor válido, de acuerdo con el criterio WCAG 2.2 - Criterio 1.3.5: Identificar Propósito del Campo de Entrada.

🧪 Objetivo  
Detectar errores relacionados con:

- Campos relevantes (nombre, email, teléfono, dirección, etc.) que **no tienen el atributo `autocomplete`**.  
- Atributos `autocomplete` presentes pero con **valores no válidos** según la especificación de HTML 5.2.

📦 Checker incluido  
Este archivo ejecuta un verificador para evaluar la accesibilidad semántica de los campos de formulario:

| Función           | Descripción                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `run_all___1_3_5` | Identifica campos de entrada que no declaran su propósito correctamente.    |

🧰 Uso de la función general

```python
from wcag_1_3_5_tester import run_all___1_3_5

issues = run_all___1_3_5(html_content, page_url)
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
WCAG 2.2 - Criterio 1.3.5: Identificar Propósito del Campo de Entrada
Guía de buenas prácticas para formularios accesibles: WAI - WCAG Input Purpose