# WCAG 3.3.1 - Error Identification Checker

Este módulo detecta campos de formulario que presentan errores de validación pero **no** muestran un mensaje de error visible o accesible, en conformidad con el criterio [WCAG 3.3.1: Error Identification](https://www.w3.org/WAI/WCAG21/Understanding/error-identification.html).

---

## ✅ ¿Qué verifica este tester?

Detecta campos de formulario que:

1. Están marcados con `aria-invalid="true"`.
2. No muestran un mensaje de error visual o accesible vinculado al campo.

---

## 🔎 Criterios de análisis

### 🔹 Búsqueda de errores visibles:

- Verifica si el campo tiene `aria-describedby` apuntando a un elemento visible con texto de error.
- Si no, busca elementos hermanos (`<span>`, `<div>`, `<p>`, `<small>`) con clases que contengan `error` y contenido visible.

Si **no se encuentra un mensaje de error**, se considera una **violación de WCAG 3.3.1**.

---

## 🔧 Función principal

```python
run_all___3_3_1(html_content: str, page_url: str, excel: str = "issue_report.xlsx") -> list
Parámetros:
html_content: Código HTML de la página a analizar.

page_url: URL o identificador de la página para el reporte.

excel: Ruta del archivo Excel a exportar (por defecto issue_report.xlsx).

📊 Formato del reporte
El reporte se exporta a Excel con las siguientes columnas:

Campo	Descripción
Title	Título del problema encontrado
Steps	Pasos para reproducir el problema
Bug Type	Tipo de error (Error Identification)
Priority	Severidad (High)
Expected Result	Qué debería suceder según WCAG
Actual Result	Qué se detectó realmente
Suggested resolution(s)	Sugerencia para resolverlo
Failed checkpoint	Criterio de accesibilidad fallido (3.3.1)
User Impact	Cómo afecta al usuario
Evidence [SS or Video]	Información del elemento con el problema
📌 Ejemplo de incidencia detectada
json
Copy
Edit
{
  "Title": "Form field missing visible error message",
  "Steps": "1. Open the page: https://example.com\n2. Locate the form field: input\n3. Trigger validation and check if error message is present and visible.",
  "Bug Type": "Error Identification",
  "Priority": "High",
  "Expected Result": "Each invalid field must have a visible and descriptive error message.",
  "Actual Result": "The field 'email' is marked as invalid but no visible error message was found.",
  "Suggested resolution(s)": "Ensure a visible text error message is placed next to the field or linked using aria-describedby.",
  "Failed checkpoint": "3.3.1",
  "User Impact": "Users may not understand what error needs correction.",
  "Evidence [SS or Video]": "input[class=form-control, id=email, name=email, line=145]"
}
📦 Requisitos
Python 3

beautifulsoup4

transform_json_to_excel (módulo auxiliar para exportación de reportes)

🧠 Recomendaciones
Siempre enlaza mensajes de error con aria-describedby.

Asegúrate de que los mensajes de error sean visibles y no estén ocultos con display: none.

Utiliza clases consistentes como error o field-error para facilitar la identificación y estilización.

Este módulo es esencial para garantizar que los errores de validación en formularios sean comprensibles para todos los usuarios, incluyendo aquellos que utilizan tecnologías asistivas.