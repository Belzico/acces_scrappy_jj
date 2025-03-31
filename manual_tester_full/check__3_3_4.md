# ✅ WCAG 3.3.4 - Error Prevention (Legal, Financial, Data)

Este script automatizado en **Python** busca formularios y botones que impliquen acciones críticas (legales, financieras o que modifiquen/borran datos del usuario) y verifica si hay palabras que indiquen confirmación, revisión o capacidad de revertir, acorde a **WCAG 3.3.4 (Nivel AA)**.

## 🧪 Objetivo
Descubrir:
- Formularios o botones con indicios de "compra", "transacción", "borrar cuenta", etc.
- Ausencia de referencias a "review", "confirm", "cancel", "undo", etc.

Si se encuentra un elemento *crítico* sin rastro de confirmación o reversión, se reporta un **posible incumplimiento**.

## 📦 Checker incluido

| Función              | Descripción                                                                                           |
|----------------------|-------------------------------------------------------------------------------------------------------|
| `run_all___3_3_4`    | Identifica acciones de alto riesgo y comprueba la falta de confirmación/reversión según WCAG 3.3.4.   |

## 🧰 Uso de la función general

```python
from check__3_3_4 import run_all___3_3_4

issues = run_all___3_3_4(html_content, page_url="http://example.com", excel="issue_report.xlsx")
Genera un archivo Excel con incidencias.
Si no hay incidencias, incluye la fila:

"Justificación de los CPs asignados que no generen issues"

📤 Formato de salida
El reporte Excel (por defecto issue_report.xlsx) incluye:

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

transform_json_to_excel (módulo personalizado)

openpyxl

📚 Referencia
WCAG 3.3.4 – Error Prevention (Legal, Financial, Data)

Guías para implementar confirmación, revisión o deshacer en acciones de alto riesgo