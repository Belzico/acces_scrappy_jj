# WCAG 1.4.12 - Text Spacing (Zoom Compatibility) Checker

Este módulo automatiza la detección de problemas relacionados con el criterio **1.4.12: Text Spacing** de [WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html), que requiere que el contenido siga siendo legible y funcional cuando se ajustan los valores de espaciado de texto del usuario.

---

## ✅ ¿Qué valida este tester?

El script identifica problemas comunes que impiden que el contenido se ajuste correctamente cuando se modifica el espaciado de texto:

### 🔍 Problemas evaluados:

- Uso de `overflow: hidden;` en menús o contenedores de texto.
- Uso de `white-space: nowrap;` que impide el ajuste del texto.
- Estilos `max-height` en píxeles que pueden truncar contenido.
- `height` en píxeles que limitan el crecimiento del contenido al aumentar el espaciado.

---

## 🔧 Función principal

```python
run_all___1_4_12(html_content: str, page_url: str, excel: str = "issue_report.xlsx") -> list
Parámetros:
html_content: HTML de la página a analizar.

page_url: URL o nombre identificador de la página.

excel: Nombre del archivo de Excel de salida.

📊 Formato del reporte
Cada incidencia se guarda en un Excel con los siguientes campos:

Campo	Descripción
Title	Título de la incidencia detectada
Steps	Pasos para inspeccionar el error
Bug Type	Categoría del error (Zoom)
Priority	Severidad (por defecto: High)
Expected Result	Qué se espera según la norma
Actual Result	Qué problema se detectó
Suggested resolution(s)	Soluciones recomendadas
Failed checkpoint	Criterio WCAG afectado (1.4.12)
User Impact	Cómo afecta al usuario final
Evidence [SS or Video]	Evidencia técnica del elemento
📌 Ejemplo de incidencia
json
Copy
Edit
{
  "Title": "Text does not wrap in the menu",
  "Bug Type": "Zoom",
  "Priority": "High",
  "Expected Result": "Text should wrap naturally when spacing increases.",
  "Actual Result": "This menu item uses `white-space: nowrap;`, preventing wrapping.",
  "Suggested resolution(s)": "Allow wrapping to avoid overflow issues.",
  "Failed checkpoint": "1.4.12",
  "User Impact": "Menu items may overflow or be unreadable.",
  "Evidence [SS or Video]": "a[class=menu-link, id=nav-about, line=88]"
}
🧠 Recomendaciones
Evita usar overflow: hidden y white-space: nowrap sin medidas de fallback.

Usa min-height: auto o unidades relativas (em, %) en lugar de valores fijos en píxeles.

Asegúrate de que todos los contenedores de texto permitan crecer dinámicamente si el usuario aplica estilos personalizados de espaciado.

📦 Dependencias
BeautifulSoup

re

transform_json_to_excel (función interna para guardar los resultados)

Este módulo forma parte del sistema automatizado de evaluación de accesibilidad conforme a WCAG 2.2, y está optimizado para detectar errores que afectan la lectura en situaciones de zoom o personalización del texto.