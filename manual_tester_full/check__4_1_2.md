# ✅ WCAG 4.1.2 - Name, Role, Value: ARIA Attribute Checker

Este script automatizado en Python analiza componentes HTML interactivos y verifica si exponen correctamente su **nombre, rol y valor** a las tecnologías de asistencia, según la norma [WCAG 2.2 - Criterio 4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html).

## 🧪 Objetivo

Detectar errores relacionados con:

- Atributos `aria-expanded`, `aria-pressed`, `aria-selected`, `aria-label`, `aria-checked`.
- Falta de nombre accesible (`aria-label`, `aria-labelledby`, o contenido textual).
- Elementos interactivos sin `role`.
- Estados no programáticamente definidos (ej. checkboxes sin `checked` ni `aria-checked`).

---

## 📦 Checkers incluidos

Este archivo agrupa múltiples funciones para auditar distintos patrones de accesibilidad:

| Función                                  | Descripción                                                                 |
|------------------------------------------|-----------------------------------------------------------------------------|
| `check_accordion_aria_expanded`          | Verifica que los botones de acordeón usen `aria-expanded`.                 |
| `check_aria_label_in_div`                | Detecta `<div>` con `aria-label` pero sin `role`.                          |
| `check_button_aria_expanded`             | Detecta botones expandibles sin `aria-expanded`.                           |
| `check_button_aria_pressed`              | Verifica que botones seleccionados usen `aria-pressed="true"`.             |
| `check_combobox_aria_expanded`           | Verifica que los `combobox` actualicen `aria-expanded`.                    |
| `check_mobile_button_aria_expanded`      | Igual que el anterior, pero pensado para botones móviles.                  |
| `check_name_role_value`                  | Evalúa accesibilidad completa: nombre, rol y valor programático.           |
| `check_tab_aria_selected`                | Verifica que las pestañas activas tengan `aria-selected="true"`.           |

---

## 🧰 Uso de la función general

```python
from check__1_4_2 import run_all___1_4_2

issues = run_all___1_4_2(html_content, page_url)
El archivo Excel generado incluirá una fila por cada incidencia detectada.

Si no se detectan errores, se incluirá una fila con una justificación positiva:
"Justificación de los CPs asignados que no generen issues".

📝 Formato de salida
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

(+ Justification si no hay errores)

📌 Requisitos
Python 3.8+

Librerías:

beautifulsoup4

openpyxl (usada por transform_json_to_excel)

📚 Referencia
WCAG 2.2 - Criterio 4.1.2

Using ARIA effectively