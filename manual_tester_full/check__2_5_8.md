# ✅ WCAG 2.5.8 - Target Size (Minimum): Verificador de Tamaños Interactivos

Este script automatizado en **Python** analiza contenido HTML en busca de elementos interactivos demasiado pequeños según el **Criterio WCAG 2.5.8 (Nivel AA)**.

## 🎯 Objetivo
Detectar elementos interactivos (`<button>`, `<a>`, `<input>`, etc.) que:
- Tienen un tamaño menor a **24x24 CSS píxeles**
- Y **no cumplen** con el criterio de espaciado suficiente

## 📦 Checker incluido

| Función           | Descripción                                                                                           |
|-------------------|-------------------------------------------------------------------------------------------------------|
| `run_all___2_5_8` | Detecta targets interactivos muy pequeños y evalúa si podrían provocar errores de activación táctil. |

## 🧰 Uso

```python
from wcag_2_5_8_tester import run_all___2_5_8

with open("example.html") as f:
    html = f.read()

issues = run_all___2_5_8(html, page_url="http://localhost", excel="issue_report.xlsx")
📤 Formato de salida
El archivo issue_report.xlsx incluye las siguientes columnas:

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

Si no se detectan problemas, se incluye una fila con:

Justificación de los CPs asignados que no generen issues

📚 Referencia
WCAG 2.1 / 2.2 - Criterio 2.5.8

Tamaño mínimo de targets interactivos para evitar errores táctiles