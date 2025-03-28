# WCAG 1.4.4 - Resize Text (Zoom 200%) Checker

Este módulo verifica el cumplimiento del criterio **1.4.4 Resize Text** de la norma [WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html), asegurando que el texto no se corte ni trunque cuando un usuario amplía el contenido al **200%**.

## ✔️ ¿Qué valida este tester?

1. **Estilos CSS problemáticos** que puedan truncar o cortar el texto al hacer zoom:
   - `overflow: hidden`
   - `height: ...`
   - `max-height: ...`

2. **Clases problemáticas** comunes utilizadas para truncar texto, tales como:
   - `hidden`
   - `truncate`
   - `text-cutoff`
   - `text-hidden`

## 📂 Función principal

```python
run_all___1_4_4(html_content: str, page_url: str, excel: str = "issue_report.xlsx") -> list
html_content: contenido HTML de la página.

page_url: URL o identificador de la página analizada.

excel: nombre del archivo de Excel de salida (opcional).

📊 Formato del reporte
Cada incidencia se reporta con los siguientes campos:

Campo	Descripción
Title	Título de la incidencia
Steps	Pasos para reproducir
Bug Type	Tipo de error (Zoom)
Priority	Severidad (High)
Expected Result	Qué se espera si cumple la norma
Actual Result	Qué se encontró que viola la norma
Suggested resolution(s)	Sugerencias para remediar el problema
Failed checkpoint	Criterio WCAG relacionado
User Impact	Impacto en usuarios con discapacidad
Evidence [SS or Video]	Evidencia técnica del elemento afectado
📌 Ejemplo de incidencia generada
json
Copy
Edit
{
  "Title": "Text may be cut off at 200% zoom",
  "Bug Type": "Zoom",
  "Priority": "High",
  "Expected Result": "Text should remain fully visible when zoomed to 200%.",
  "Actual Result": "Element uses `overflow: hidden`, `height`, or `max-height` which may cause clipping.",
  "Suggested resolution(s)": "Avoid fixed height/overflow on text containers. Use flexible layouts.",
  "Failed checkpoint": "1.4.4",
  "User Impact": "Important information may be lost during zoom.",
  "Evidence [SS or Video]": "div[class=card-description, line=102]"
}
🧪 Tecnologías utilizadas
BeautifulSoup para parseo HTML.

transform_json_to_excel para exportar a Excel.

Estilo y estructura consistente con otros testers WCAG.

🧠 Recomendaciones
No usar overflow: hidden; en contenedores críticos de contenido.

Evitar truncar texto con clases como truncate o text-cutoff.

Usar min-height, max-width, flex, y wrap para permitir crecimiento de texto al hacer zoom.

Módulo desarrollado para auditorías automáticas de accesibilidad bajo WCAG 2.2.