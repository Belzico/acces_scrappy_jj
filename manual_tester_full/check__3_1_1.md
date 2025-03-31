# ✅ WCAG 3.1.1 - Language of Page: Verificador del Idioma Predeterminado

Este script automatizado en **Python** analiza si una página HTML especifica correctamente el **idioma predeterminado** usando el atributo `lang` en la etiqueta `<html>`, como requiere el **criterio WCAG 3.1.1 (Nivel A)**.

## 🧪 Objetivo
Detectar si el idioma principal de una página puede ser **determinado automáticamente** por tecnologías de asistencia como lectores de pantalla.

## 📦 Checker incluido

| Función           | Descripción                                                                                      |
|-------------------|--------------------------------------------------------------------------------------------------|
| `run_all___3_1_1` | Verifica si el elemento `<html>` contiene un atributo `lang` con un valor válido (ej. `lang="en"`). |

## 📌 ¿Por qué es importante?
Un `lang` correctamente definido permite a los lectores de pantalla:
- Utilizar reglas de pronunciación adecuadas.
- Leer el contenido en el idioma esperado por el usuario.
- Mejorar la comprensión para personas con discapacidades cognitivas o lingüísticas.

## 🧰 Uso de la función

```python
from wcag_3_1_1_tester import run_all___3_1_1

issues = run_all___3_1_1(html_content, page_url, excel="issue_report.xlsx")
🧾 Formato del reporte Excel
Incluye los siguientes campos:

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
WCAG 2.1 / 2.2 - Criterio 3.1.1: Language of Page

Recomendación de buenas prácticas: W3C i18n Best Practices