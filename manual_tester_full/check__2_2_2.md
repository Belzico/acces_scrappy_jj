# ✅ WCAG 2.2.2 - Pause, Stop, Hide: Verificador de Contenido en Movimiento

Este script automatizado en **Python** analiza contenido HTML en busca de **elementos que se mueven, parpadean o actualizan automáticamente**, según el **Criterio WCAG 2.2.2 (Nivel A)**.

## 🧪 Objetivo
Detectar:
- Animaciones, desplazamientos o actualizaciones automáticas.
- Que **no puedan pausarse, detenerse o esconderse** por el usuario.

## 📦 Checker incluido

| Función           | Descripción                                                                                                     |
|-------------------|-----------------------------------------------------------------------------------------------------------------|
| `run_all___2_2_2` | Busca elementos como `<marquee>`, estilos con `animation`, o atributos como `scrollamount` sin controles visibles. |

## 🧰 Uso

```python
from wcag_2_2_2_tester import run_all___2_2_2

issues = run_all___2_2_2(html_content, page_url, excel="issue_report.xlsx")
📤 Salida
Un archivo Excel con columnas:

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

Si no hay problemas, se incluye una fila de justificación.

📚 Referencia
WCAG 2.1 / 2.2 - Criterio 2.2.2: Pause, Stop, Hide