# ✅ WCAG 3.2.2 - On Input: Verificador de Cambios de Contexto

Este script en **Python** analiza el contenido HTML para identificar controles de formulario (select, radio, checkbox) que pueden producir un cambio de contexto – p. ej., abrir una ventana o redirigir – **en cuanto** el usuario modifica el valor, incumpliendo **WCAG 3.2.2** si no hay un aviso o confirmación previa.

## 🧪 Objetivo
- Detectar `<select>` con `onchange="location.href=..."` o `onchange="form.submit()"`, etc.
- Detectar `<input type="radio"|"checkbox">` con `onchange/onclick="window.open(...)"`, etc.
- Avisar si se hallan patrones indicando **posible cambio de contexto** sin confirmación.

## 📦 Checker incluido

| **Función**             | **Descripción**                                                                                                                             |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `run_all___3_2_2`       | Revisa `<select>` y `<input type=radio|checkbox>` en busca de scripts que llamen `window.open`, `location.href`, etc. en `onchange` u `onclick`.|

## 🧰 Uso de la función general

```python
from check__3_2_2 import run_all___3_2_2

issues = run_all___3_2_2(html_content, page_url="http://example.com", excel="issue_report.xlsx")
Se genera un archivo Excel con las incidencias detectadas.
Si no hay incidencias, se agrega la fila:

"Justificación de los CPs asignados que no generen issues"

📤 Formato de salida
El Excel (por defecto issue_report.xlsx) incluye columnas:

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

transform_json_to_excel

📚 Referencia
WCAG 2.1/2.2 - 3.2.2 On Input

Buenas prácticas: permitir que el usuario confíe en que cambiar un control no recarga la página instantáneamente sin un aviso.