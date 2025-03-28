# 🧪 Tester WCAG 1.3.1 – Info and Relationships

Este tester verifica que las **estructuras semánticas** y **relaciones informativas** estén correctamente definidas en el HTML para cumplir con el criterio **WCAG 1.3.1 - Info and Relationships (Nivel A)**.

---

## 📌 ¿Qué verifica?

El criterio 1.3.1 exige que **la estructura del contenido y las relaciones visuales también sean detectables mediante código**, de modo que tecnologías como lectores de pantalla puedan interpretarlas correctamente.

Este tester analiza:

- ❌ Encabezados simulados con `<div>`, `<span>` o clases como `"title"`, en lugar de usar `<h1>` a `<h6>`
- ❌ Listas visuales simuladas con `*` o `-` pero sin usar `<ul>`, `<ol>`, `<li>`
- ❌ Uso de tablas de datos sin `<th>`, `scope`, `caption`, o relaciones programáticas
- ❌ Campos de formulario sin `<label>` o sin atributos `for`
- ❌ Agrupaciones visuales de campos sin `fieldset` ni `legend`

---

## ✅ Criterio WCAG

**Criterio:** [1.3.1 – Info and Relationships](https://www.w3.org/WAI/WCAG21/Understanding/info-and-relationships.html)

> La información, estructura y relaciones presentadas visual o auditivamente deben poder determinarse mediante código o estar disponibles en texto.

---

## 🧪 Cómo funciona

El tester escanea el HTML y reporta:

- Elementos que deberían tener etiquetas semánticas (como encabezados o listas) pero no las tienen.
- Campos de formulario sin etiqueta asociada.
- Tablas que parecen de datos pero carecen de encabezados.
- Agrupaciones visuales de campos de formulario sin `fieldset` y `legend`.

---

## 📤 Resultado

Genera un archivo Excel con columnas como:

- **Title**: Breve título del problema
- **Steps**: Pasos para reproducir el hallazgo
- **Bug Type**: Tipo de problema detectado
- **Priority**: Severidad estimada
- **Expected Result**: Comportamiento accesible esperado
- **Actual Result**: Lo que se encontró en el HTML
- **Suggested resolution(s)**: Cómo solucionar el problema
- **Failed checkpoint**: Criterio WCAG relacionado (1.3.1)
- **User Impact**: Consecuencias para usuarios con discapacidad
- **Evidence**: Referencia al elemento HTML afectado

---

## 🧪 Ejecución

Desde tu script principal o desde `global_tester.py`, puedes llamar:

```python
from testers.testers_1_3_1 import run_all___1_3_1

run_all___1_3_1(html_content, page_url, excel="issue_report.xlsx")
📄 HTML de prueba
Un ejemplo de HTML con errores para este tester lo encuentras en samples/sample_1_3_1.html.

💡 Recomendaciones
Usa siempre etiquetas semánticas para listas, encabezados, tablas, formularios.

No confíes solo en estilos visuales como color, tamaño o posición.

Relaciona los campos del formulario con sus etiquetas mediante for y id.

📚 Recursos
WCAG 1.3.1 – Understanding Info and Relationships

MDN Web Docs – HTML Semantic Elements

WebAIM – Semantic Structure