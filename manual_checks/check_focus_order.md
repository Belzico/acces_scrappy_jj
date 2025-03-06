# 🔍 Focus Order Tester - `check_focus_order.py`

Este script detecta **problemas en el orden de navegación del foco** en elementos interactivos y modales.  
Garantiza que los usuarios de teclado puedan navegar de manera lógica y predecible a través de los elementos de una página web.  

## 📌 ¿Por qué es importante?
Según las **Directrices de Accesibilidad para el Contenido Web (WCAG)**, el foco debe seguir un orden **natural y predecible**.  
Si el foco no está correctamente gestionado, puede generar problemas como:

- ❌ **Los usuarios de teclado pueden perderse en la navegación.**
- ❌ **Los elementos interactivos pueden ser inaccesibles.**
- ❌ **Los modales pueden no gestionar correctamente el foco.**

---

## ⚠️ **Problemas Detectados**
El script analiza y reporta los siguientes problemas de accesibilidad:

1️⃣ **Uso de `tabindex` mayor a 0**  
   - Puede interrumpir el orden natural de navegación.  
   - **Ejemplo incorrecto:**  
   ```html
   <button tabindex="5">Click Me</button>
Solución:
html
Copy
Edit
<button>Click Me</button>
2️⃣ Elementos interactivos con tabindex="-1"

Hacen que botones, enlaces o inputs sean inaccesibles con el teclado.
Ejemplo incorrecto:
html
Copy
Edit
<a href="page.html" tabindex="-1">Go to Page</a>
Solución:
html
Copy
Edit
<a href="page.html" tabindex="0">Go to Page</a>
3️⃣ Enlaces sin href y sin tabindex

No son alcanzables mediante Tab.
Ejemplo incorrecto:
html
Copy
Edit
<a>Learn More</a>
Solución:
html
Copy
Edit
<a href="page.html">Learn More</a>
4️⃣ Modales (<dialog>) sin atributo open

Pueden no gestionar correctamente el foco cuando están visibles.
Ejemplo incorrecto:
html
Copy
Edit
<dialog>Content</dialog>
Solución:
html
Copy
Edit
<dialog open>Content</dialog>
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
from check_focus_order import check_focus_order

with open("test_focus_order.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///ruta/del/archivo/test_focus_order.html"
incidencias = check_focus_order(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si se encuentra un problema en la gestión del foco, el tester reportará:

json
Copy
Edit
{
    "title": "Use of tabindex greater than 0",
    "type": "Focus Order",
    "severity": "High",
    "description": "The element has tabindex=5, which can disrupt the natural focus order.",
    "remediation": "Avoid using tabindex greater than 0. Use the natural DOM order.",
    "wcag_reference": "2.4.3",
    "impact": "The focus order may become unpredictable.",
    "page_url": "file:///ruta/del/archivo/test_focus_order.html",
    "resolution": "check_focus_order.md",
    "element_info": {
        "tag": "button",
        "id": "N/A",
        "class": "btn-primary",
        "line_number": 15
    }
}
✅ Beneficios del Tester
✔ Detecta problemas en el orden de navegación del foco.
✔ Muestra los elementos afectados y su código.
✔ Mejora la accesibilidad para usuarios de teclado.
✔ Fácil integración con global_tester.py.

💡 ¡Con este tester garantizamos una navegación accesible y predecible! 🚀