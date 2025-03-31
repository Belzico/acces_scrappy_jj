# ✅ WCAG 2.4.4 - Link Purpose (In Context): Verificador de Texto de Enlaces

Este script automatizado en **Python** analiza el contenido HTML para verificar que los enlaces tengan un texto lo suficientemente descriptivo, de acuerdo con el **Criterio WCAG 2.4.4 (Nivel A)**.

## 🧪 Objetivo
Detectar errores relacionados con:
- Enlaces cuyo texto sea ambiguo o genérico (por ej. "click here", "read more").
- Enlaces **sin texto** alguno (que resultan imposibles de identificar para lectores de pantalla).

## 📦 Checker incluido
Este archivo ejecuta un verificador para evaluar la accesibilidad de los enlaces:

| Función           | Descripción                                                                                            |
|-------------------|--------------------------------------------------------------------------------------------------------|
| `run_all___2_4_4` | Identifica los enlaces que no describen el propósito de forma clara, o que no tienen texto alguno.     |

## 🧰 Uso de la función general

```python
from wcag_2_4_4_tester import run_all___2_4_4

issues = run_all___2_4_4(html_content, page_url, excel="issue_report_2_4_4.xlsx")
El archivo Excel generado incluirá una fila por cada incidencia detectada.
Si no se detectan errores, se incluirá una fila con la justificación positiva: "Justificación de los CPs asignados que no generen issues".

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
WCAG 2.1 / 2.2 - Criterio 2.4.4: Link Purpose (In Context)

Understanding Success Criterion 2.4.4

Guías sobre accesibilidad de enlaces y buenas prácticas de redacción de texto linkeable