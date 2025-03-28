# ✅ WCAG 1.1.1 - Alternative Text: Image & Icon Checker

Este script automatizado en Python analiza el contenido HTML para verificar el uso adecuado de texto alternativo en imágenes e íconos, de acuerdo con el criterio [WCAG 2.2 - Criterio 1.1.1: Contenido no textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html).

## 🧪 Objetivo

Detectar errores relacionados con:

- Imágenes sin atributo `alt`.
- Imágenes con `alt=""` que forman parte de enlaces o botones sin texto accesible.
- Texto alternativo redundante que duplica contenido adyacente.
- Íconos informativos sin `aria-label`, `aria-hidden="true"` o texto visible.

---

## 📦 Checkers incluidos

Este archivo agrupa múltiples funciones para auditar distintos patrones de accesibilidad relacionados con el texto alternativo:

| Función                        | Descripción                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `check_alt_distinction`       | Evalúa si el `alt` está ausente, vacío en contextos críticos o es redundante.|
| `check_icons_informative`     | Verifica que íconos con significado tengan texto accesible o `aria-label`.  |
| `check_images_decorative`     | Detecta imágenes sin `alt`, incluyendo decorativas que deberían tener `alt=""`.|
| `check_informative_images`    | Detecta imágenes informativas con `alt` vacío o ausente.                    |

---

## 🧰 Uso de la función general

```python
from check__1_1_1 import run_all___1_1_1

issues = run_all___1_1_1(html_content, page_url)
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

Librerías necesarias:

beautifulsoup4

openpyxl (usada por transform_json_to_excel)

sentence-transformers

torch

Pillow (opcional, si se usa OCR con pytesseract)

pytesseract (opcional)

📚 Referencia
WCAG 2.2 - Criterio 1.1.1: Contenido no textual

Guía de uso de texto alternativo (WAI)