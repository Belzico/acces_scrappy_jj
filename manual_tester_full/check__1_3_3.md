# ✅ WCAG 1.3.3 - Sensory Characteristics: Verificador de Instrucciones

Este script automatizado en **Python** analiza el contenido HTML para verificar que las instrucciones de uso **no dependan únicamente** de características sensoriales (posición, color, forma, etc.), de acuerdo con el **Criterio WCAG 1.3.3: Sensory Characteristics (Nivel A)**.

## 🧪 Objetivo
Detectar errores relacionados con:

- Instrucciones que usan **solo** color, forma o ubicación para describir un elemento interactivo.  
- Ausencia de referencias textuales o etiquetas (ej. `"label"`, `'titled'`, etc.) que ayuden a identificar controles.  

De esta manera, se asegura que las personas con discapacidades visuales y las que emplean lectores de pantalla (o tecnologías asistivas similares) puedan comprender las acciones a realizar sin depender de información visual.

## 📦 Checker incluido
Este archivo ejecuta un verificador para evaluar la accesibilidad semántica de las instrucciones:

| **Función**       | **Descripción**                                                                                                                     |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| `run_all___1_3_3` | Revisa el contenido HTML y detecta aquellas instrucciones que dependen solo de pistas sensoriales.                                  |

## 🧰 Uso de la función general

```python
from wcag_1_3_3_tester import run_all___1_3_3

issues = run_all___1_3_3(html_content, page_url, excel="issue_report_1_3_3.xlsx")
html_content: Cadena con el contenido HTML a analizar.

page_url: (Opcional) URL de la página donde se tomó el HTML, para mayor contexto en el reporte.

excel: Nombre del archivo Excel que se generará (por defecto "issue_report_1_3_3.xlsx").

El archivo Excel generado incluirá una fila por cada incidencia detectada.
Si no se detectan errores, el reporte mostrará una fila con la justificación positiva:
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

Evidence [SS or Video]

(Si no se detectan problemas, se incluye una fila con la justificación).

📌 Requisitos
Python 3.8+

Librerías necesarias:

beautifulsoup4

openpyxl (usada por transform_json_to_excel)

transform_json_to_excel (módulo personalizado de exportación a Excel)

📚 Referencia
WCAG 2.1 / 2.2 - Criterio 1.3.3: Sensory Characteristics

Understanding Success Criterion 1.3.3

Guía sobre accesibilidad y eliminación de barreras visuales, cognitivas y de percepción.

Copy
Edit
