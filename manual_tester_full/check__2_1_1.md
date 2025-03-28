# WCAG 2.1.1 - Keyboard Accessibility Checker

Este módulo automatiza la detección de elementos y scripts que no pueden ser activados o accedidos mediante teclado, conforme al criterio **2.1.1: Keyboard** de [WCAG 2.2](https://www.w3.org/WAI/WCAG21/Understanding/keyboard.html).

---

## ✅ ¿Qué valida este tester?

### 1️⃣ Interactividad con el teclado

Identifica elementos HTML que:

- Tienen `onclick`, `onmouseover`, `onmouseenter`, pero **no tienen** `onkeydown`, `onkeypress` o `onfocus`.
- Son `div` o `span` interactivos sin `tabindex='0'`.

### 2️⃣ JavaScript sin soporte de teclado

Escanea el contenido de scripts `<script>` para detectar:

- `.addEventListener('click')` sin su equivalente `keydown`.
- `.addEventListener('mouseover' | 'mouseenter')` sin `focus`.
- `display: none` aplicado por JavaScript sin `aria-hidden="true"`.

### 3️⃣ Atributos personalizados `data-event="mouseover"`

Detecta si falta `onfocus` para accesibilidad por teclado.

---

## 🔧 Función principal

```python
run_all___2_1_1(html_content: str, page_url: str, excel: str = "issue_report.xlsx") -> list
Parámetros:
html_content: Código HTML de entrada (como cadena).

page_url: URL o identificador de la página evaluada.

excel: Ruta del archivo Excel de salida (por defecto: issue_report.xlsx).

📊 Formato del reporte
Cada incidencia se transforma en una fila de Excel con los siguientes campos:

Campo	Descripción
Title	Título del problema
Steps	Instrucciones para reproducirlo
Bug Type	Categoría (ej. "Keyboard Accessibility")
Priority	Severidad (High, Medium, Low)
Expected Result	Qué se espera según WCAG
Actual Result	Qué se detectó realmente
Suggested resolution(s)	Acción recomendada
Failed checkpoint	Criterio WCAG aplicable (2.1.1)
User Impact	Consecuencia para el usuario
Evidence [SS or Video]	Descripción técnica del elemento afectado
📌 Ejemplo de incidencia
json
Copy
Edit
{
  "Title": "Element with mouse events but no keyboard support",
  "Bug Type": "Keyboard Accessibility",
  "Priority": "High",
  "Expected Result": "Interactive elements must respond to keyboard inputs such as onkeydown.",
  "Actual Result": "The element uses onclick but lacks keyboard equivalents: onkeydown.",
  "Suggested resolution(s)": "Add handlers for onkeydown to make it keyboard accessible.",
  "Failed checkpoint": "2.1.1",
  "User Impact": "Users who rely on keyboard cannot interact with this element.",
  "Evidence [SS or Video]": "div[class=card-button, id=mainCard, line=134]"
}
🧠 Recomendaciones
Usa siempre onkeydown o onkeypress junto con onclick.

Para scripts JS, agrega también addEventListener('keydown') si usas click.

Usa tabindex="0" en div o span interactivos.

Oculta contenido con aria-hidden="true" si usas display: none.

📦 Dependencias
BeautifulSoup

re

transform_json_to_excel (utilidad interna para exportar reportes)

Este módulo permite asegurar que toda la funcionalidad ofrecida mediante el mouse también esté disponible mediante el teclado, garantizando accesibilidad para usuarios con movilidad reducida o que usan tecnologías asistivas.