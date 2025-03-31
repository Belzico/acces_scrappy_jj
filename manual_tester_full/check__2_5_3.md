# ✅ WCAG 2.5.3 - Label in Name: Verificador de Controles

Este script automatizado en **Python** analiza el contenido HTML para verificar que los controles con un texto visible incluyan ese texto en su nombre accesible, de acuerdo con el **Criterio WCAG 2.5.3 (Nivel A)**.

## 🧪 Objetivo
Detectar errores relacionados con:
- Botones `<button>` cuyo `aria-label` no contenga el texto visible.
- Controles `<input type="button"|"submit"|"reset"|"image">` cuyo `aria-label` no coincida con el `value`/`alt`.
- Campos de formulario donde `<label>` visible difiere del `aria-label` del control asociado.

## 📦 Checker incluido
Este archivo ejecuta un verificador para evaluar la correspondencia entre la etiqueta visual y el nombre accesible:

| Función           | Descripción                                                                                                                   |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `run_all___2_5_3` | Revisa `<button>`, `<input>` tipo botón y parejas `<label for="..."> + <input id="...">`, reportando incongruencias de texto. |

## 🧰 Uso de la función general

```python
from wcag_2_5_3_tester import run_all___2_5_3

issues = run_all___2_5_3(html_content, page_url, excel="issue_report.xlsx")
El archivo Excel generado incluirá una fila por cada incidencia detectada. Si no se detectan errores, se incluirá una fila con la justificación: "Justificación de los CPs asignados que no generen issues".

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
WCAG 2.1 / 2.2 - Criterio 2.5.3: Label in Name

Understanding Success Criterion 2.5.3

Guías sobre accesibilidad de controles con el mismo nombre visible y accesible