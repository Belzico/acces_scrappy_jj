# ✅ WCAG 3.2.1 - On Focus: Verificador de Cambios de Contexto

Este script en **Python** analiza el contenido HTML y detecta elementos con `onfocus` cuyo código podría iniciar un cambio de contexto automáticamente, incumpliendo la pauta **WCAG 3.2.1 (Nivel A)**.

## 🧪 Objetivo
Descubrir:
- Elementos que usan `onfocus="..."` con acciones como:
  - `window.open(...)`
  - `location.href=...`
  - `this.form.submit()`
- Dichas acciones **pueden** redirigir, abrir ventana nueva o cambiar foco, causando un **cambio de contexto** inesperado.

## 📦 Checker incluido

| **Función**             | **Descripción**                                                                                                                    |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `run_all___3_2_1`       | Revisa todos los elementos con `onfocus` y reporta si el contenido coincide con patrones que implican un cambio de contexto.       |

## 🧰 Uso de la función general

```python
from check__3_2_1 import run_all___3_2_1

issues = run_all___3_2_1(html_content, page_url="http://example.com", excel="issue_report.xlsx")
El archivo Excel resultante incluirá una fila por cada incidencia identificada.
Si no hay incidencias, se crea la fila:

"Justificación de los CPs asignados que no generen issues".

📤 Formato de salida
Las columnas de reporte incluyen:

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
WCAG 2.1 / 2.2 - 3.2.1 On Focus

Buenas prácticas: no disparar cambios de ventana o redirecciones solo al recibir foco.