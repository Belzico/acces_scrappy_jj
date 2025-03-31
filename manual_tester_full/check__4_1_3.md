# ✅ WCAG 4.1.3 - Status Messages: Verificador de Roles/Live Regions

Este script automatizado en **Python** analiza el contenido HTML para detectar posibles mensajes de estado que **no** cuenten con propiedades o roles ARIA que permitan a los lectores de pantalla anunciarlos, según el **Criterio WCAG 4.1.3 (Nivel AA)**.

## 🧪 Objetivo
Descubrir problemas relacionados con:
- Texto que parece ser un **mensaje de estado** (palabras clave como "error", "success", "loading", etc.) pero **sin** `role="status"`/`role="alert"`/`aria-live="polite|assertive"`.
- Los usuarios con **screen readers** podrían **no** enterarse de los cambios de contenido que no toman el foco.

## 📦 Checker incluido
Este archivo ejecuta un verificador para evaluar el marcado ARIA de los mensajes:

| Función           | Descripción                                                                                              |
|-------------------|----------------------------------------------------------------------------------------------------------|
| `run_all___4_1_3` | Identifica bloques de texto con keywords de estado sin `role` o `aria-live` que notifiquen el cambio.    |

## 🧰 Uso de la función general

```python
from wcag_4_1_3_tester import run_all___4_1_3

issues = run_all___4_1_3(html_content, page_url, excel="issue_report.xlsx")
El archivo Excel generado incluirá una fila por cada incidencia detectada.
Si no se detectan errores, se incluirá una fila con la justificación positiva: "Justificación de los CPs asignados que no generen issues."

📤 Formato de salida
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

Evidence [SS or Video]

📌 Requisitos
Python 3.8+

Librerías necesarias:

beautifulsoup4

openpyxl (usada por transform_json_to_excel)

transform_json_to_excel (módulo personalizado de exportación a Excel)

📚 Referencia
WCAG 2.1 / 2.2 - Criterio 4.1.3: Status Messages

Understanding Success Criterion 4.1.3

Guías sobre uso de roles ARIA (role="status", role="alert", aria-live) para notificaciones automáticas