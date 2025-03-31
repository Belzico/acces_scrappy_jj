# ✅ WCAG 2.2.1 - Timing Adjustable: Verificador de Límites de Tiempo

Este script automatizado en **Python** analiza contenido HTML para detectar límites de tiempo automáticos, como redirecciones o expiraciones que no permiten al usuario controlar su duración, según el **Criterio WCAG 2.2.1 (Nivel A)**.

## 🧪 Objetivo
Detectar si existen límites de tiempo:
- Por redirección automática (`<meta http-equiv="refresh">`)
- Que no ofrecen opción de apagar, extender o ajustar el tiempo.

## 📦 Checker incluido

| Función           | Descripción                                                                                       |
|-------------------|---------------------------------------------------------------------------------------------------|
| `run_all___2_2_1` | Busca etiquetas `<meta>` de refresco que imponen límites de tiempo sin control para el usuario.  |

## 🧰 Uso

```python
from wcag_2_2_1_tester import run_all___2_2_1

issues = run_all___2_2_1(html_content, page_url, excel="issue_report.xlsx")
El archivo Excel generado incluirá una fila por cada incidencia. Si no se detectan problemas, se incluirá una justificación positiva.

📤 Formato de salida
El archivo issue_report.xlsx incluye:

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

📚 Referencia
WCAG 2.2 - SC 2.2.1: Timing Adjustable