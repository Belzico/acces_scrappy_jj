# 🔍 Focus Visibility Tester - `check_focus_visible.py`

Este script detecta **problemas de visibilidad del foco** en elementos interactivos.  
Garantiza que los usuarios de teclado puedan identificar visualmente qué elemento está enfocado en cada momento.

## 📌 ¿Por qué es importante?
Según las **Directrices de Accesibilidad para el Contenido Web (WCAG)**, los usuarios que navegan mediante teclado deben poder ver claramente qué elemento tiene el foco.  
Si la visibilidad del foco no está bien gestionada, pueden ocurrir los siguientes problemas:

- ❌ **Usuarios de teclado no sabrán qué elemento está activo.**
- ❌ **Algunos elementos interactivos pueden ser inaccesibles.**
- ❌ **El foco puede perderse en la navegación.**

---

## ⚠️ **Problemas Detectados**
El script analiza y reporta los siguientes problemas de accesibilidad:

### 1️⃣ **Elementos sin indicador visible de foco**
   - **Detecta elementos que ocultan el foco con `outline: none`, `border: none`, etc.**
   - **Ejemplo incorrecto:**  
   ```html
   <button style="outline: none;">Click Me</button>
Solución:
css
Copy
Edit
button:focus {
    outline: 2px solid #000;
}
2️⃣ Elementos interactivos sin tabindex adecuado
Detecta div o span con onclick o role que no tienen tabindex=0.
Ejemplo incorrecto:
html
Copy
Edit
<div role="button" onclick="doSomething()">Click Me</div>
Solución:
html
Copy
Edit
<div role="button" onclick="doSomething()" tabindex="0">Click Me</div>
3️⃣ Elementos con tabindex="-1"
Hace que los elementos sean inaccesibles con el teclado.
Ejemplo incorrecto:
html
Copy
Edit
<button tabindex="-1">Click Me</button>
Solución:
html
Copy
Edit
<button>Click Me</button>
4️⃣ Elementos que se ocultan al recibir foco
Si un elemento desaparece con display: none o visibility: hidden cuando recibe foco, los usuarios pueden perder la referencia.
Ejemplo incorrecto:
html
Copy
Edit
<input onfocus="this.style.display='none';">
Solución:
html
Copy
Edit
<input onfocus="this.style.backgroundColor='#ff0';">
🚀 Cómo Usar el Tester
📌 Instalación
Asegúrate de tener BeautifulSoup instalado:

bash
Copy
Edit
pip install beautifulsoup4
📌 Ejecutar el Tester en un Archivo HTML
python
Copy
Edit
from check_focus_visible import check_focus_visible

with open("test_focus_visible.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///ruta/del/archivo/test_focus_visible.html"
incidencias = check_focus_visible(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si se encuentra un problema en la visibilidad del foco, el tester reportará:

json
Copy
Edit
{
    "title": "Element without visible focus indicator",
    "type": "Focus Visibility",
    "severity": "High",
    "description": "The element uses CSS styles that remove focus visibility.",
    "remediation": "Ensure focus is visible by adding `:focus` or `:focus-visible` in CSS.",
    "wcag_reference": "2.4.7",
    "impact": "Keyboard users cannot see which element is focused.",
    "page_url": "file:///ruta/del/archivo/test_focus_visible.html",
    "resolution": "check_focus_visible.md",
    "element_info": {
        "tag": "button",
        "id": "N/A",
        "class": "btn-primary",
        "line_number": 22
    }
}
✅ Beneficios del Tester
✔ Detecta elementos interactivos sin indicador de foco visible.
✔ Reporta problemas con tabindex y accesibilidad del foco.
✔ Mejora la navegación para usuarios de teclado.
✔ Fácil integración con global_tester.py.

💡 ¡Con este tester garantizamos una navegación accesible y clara para todos los usuarios! 🚀