# ✅ WCAG 3.3.3 - Error Suggestion: Verificador

Este script automatizado en **Python** revisa el contenido HTML en busca de mensajes de error que no proveen sugerencias de corrección, de acuerdo con el **Criterio WCAG 3.3.3 (Nivel AA)**.

## 🧪 Objetivo
Detectar:
1. Mensajes de error (palabras como "error", "invalid", "incorrecto", etc.).
2. Falta de palabras que indiquen **cómo** corregir (ejemplo: "ingrese", "use el formato", "should be", "please enter", etc.).

## 📦 Checker incluido

| **Función**           | **Descripción**                                                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------------------------|
| `run_all___3_3_3`     | Examina elementos HTML (p, div, span, etc.) y reporta si encuentra error messages sin sugerencia de corrección. |

## 🧰 Uso de la función general

```python
from check__3_3_3 import run_all___3_3_3

issues = run_all___3_3_3(html_content, page_url="http://example.com", excel="issue_report.xlsx")
Si detecta incidencias, genera filas con el detalle de cada una.
Si no hay incidencias, agrega la fila:

"Justificación de los CPs asignados que no generen issues"

📤 Formato de salida
El archivo Excel (por defecto issue_report.xlsx) incluye:

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

⚠️ Nota sobre IA
Este método se basa en coincidencia de cadenas para detectar la ausencia de sugerencias. La mejor manera de lograr alta precisión es entrenar un modelo de Procesamiento del Lenguaje Natural (NLP) que clasifique los mensajes de error en “con sugerencia” o “sin sugerencia” de forma más inteligente (por ejemplo, un clasificador supervisado o un enfoque zero-shot con un modelo pre-entrenado).

📌 Requisitos
Python 3.8+

beautifulsoup4

transform_json_to_excel (módulo personalizado de exportación a Excel)

openpyxl (usada internamente por transform_json_to_excel)

📚 Referencia
WCAG 3.3.3: Error Suggestion

Documentación adicional sobre buenas prácticas de mensajes de error accesibles e inclusivos.