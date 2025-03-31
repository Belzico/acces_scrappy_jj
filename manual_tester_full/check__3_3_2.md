# ✅ WCAG 3.3.2 - Labels or Instructions: Verificador Automático

Este script en Python analiza el contenido HTML para verificar que cada campo de formulario (inputs, selects, textareas) tenga **algún tipo de label** o **instrucción** visible, de acuerdo con **Criterio WCAG 3.3.2 (Nivel A)**.

## 🧪 Objetivo
Descubrir campos que:
1. Requieren user input (p. ej., `<input type="text">`, `<select>`, `<textarea>`),
2. No poseen `label` asociado (`<label for="id">`), ni `aria-label`, ni `aria-labelledby`, ni `placeholder`.

Tales campos **podrían** carecer de descripción clara de qué se espera que el usuario introduzca.

## 📦 Checker incluido

| **Función**            | **Descripción**                                                                                                |
|------------------------|----------------------------------------------------------------------------------------------------------------|
| `run_all___3_3_2`      | Identifica formularios y campos sin texto explicativo (label, placeholder o aria-label).                        |

## 🧰 Uso de la función general

```python
from check__3_3_2 import run_all___3_3_2

issues = run_all___3_3_2(html_content, page_url="http://example.com", excel="issue_report.xlsx")
Si hay incidencias, se genera una fila por cada campo conflictivo.
Si no las hay, se incluye la fila:

"Justificación de los CPs asignados que no generen issues"

📤 Formato de salida
El archivo Excel (por defecto issue_report.xlsx) incluye las columnas:

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

beautifulsoup4

openpyxl

transform_json_to_excel (módulo personalizado de exportación)

📚 Referencia
WCAG 3.3.2: Labels or Instructions (Nivel A)

Buenas prácticas: Uso de <label> o instrucciones en campos, placeholders como pista adicional, etc.