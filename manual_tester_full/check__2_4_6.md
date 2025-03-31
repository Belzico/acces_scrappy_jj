# ✅ WCAG 2.4.6 - Headings and Labels: Verificador de Descriptividad

Este script automatizado en **Python** analiza el contenido HTML para verificar que los encabezados y etiquetas existentes no sean ambiguos ni genéricos, de acuerdo con el **Criterio WCAG 2.4.6 (Nivel AA)**.

## 🧪 Objetivo
Detectar errores relacionados con:
- Encabezados (`<h1>`...`<h6>`) que están **vacíos** o usan **términos genéricos** ("Heading", "Title", "Untitled", etc.).
- Etiquetas de formularios (`<label>`) que estén **vacías** o con texto genérico ("Label", "Form Label", etc.).

## 📦 Checker incluido
Este archivo ejecuta un verificador para evaluar la claridad de encabezados y labels:

| Función           | Descripción                                                                                          |
|-------------------|------------------------------------------------------------------------------------------------------|
| `run_all___2_4_6` | Identifica los headings o labels no descriptivos (vacíos o genéricos).                                |

## 🧰 Uso de la función general

```python
from wcag_2_4_6_tester import run_all___2_4_6

issues = run_all___2_4_6(html_content, page_url, excel="issue_report.xlsx")
El archivo Excel generado incluirá una fila por cada incidencia detectada. Si no se detectan errores, se incluirá una fila con la justificación: "Justificación de los CPs asignados que no generen issues."

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

📌 Requisitos
Python 3.8+

Librerías necesarias:

beautifulsoup4

openpyxl (usada por transform_json_to_excel)

transform_json_to_excel (módulo personalizado de exportación a Excel)

📚 Referencia
WCAG 2.1 / 2.2 - Criterio 2.4.6: Headings and Labels

Understanding Success Criterion 2.4.6

Guías sobre buenas prácticas de estructuración de contenido y etiquetado de formularios


