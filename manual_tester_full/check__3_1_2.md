# ✅ WCAG 3.1.2 - Language of Parts: Verificador de Idiomas Internos

Este script en **Python** detecta frases o fragmentos en diferentes idiomas que **no estén marcados adecuadamente con el atributo `lang`**, según el **Criterio WCAG 3.1.2 (Nivel AA)**.

---

## 🎯 Objetivo
Detectar problemas de accesibilidad cuando:
- Se usa más de un idioma en una página web.
- No se identifican los cambios de idioma mediante el atributo `lang`.

---

## 📦 Checker incluido

| Función            | Descripción                                                                                             |
|--------------------|---------------------------------------------------------------------------------------------------------|
| `run_all___3_1_2`  | Busca textos en idiomas diferentes al principal sin atributo `lang`, o con `lang` no válido.           |

---

## 🧰 Uso de la función general

```python
from wcag_3_1_2_tester import run_all___3_1_2

issues = run_all___3_1_2(html_content, page_url, excel="issue_report.xlsx")
📤 Formato de salida
El archivo Excel contiene:

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

transform_json_to_excel.py (módulo personalizado)

📚 Referencia
WCAG 2.1 / 2.2 - Criterio 3.1.2: Language of Parts