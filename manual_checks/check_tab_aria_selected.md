📌 README.md
md
Copy
Edit
# 🔍 Tab Selected State Accessibility Checker

Este script verifica si el **estado seleccionado** de una pestaña (`role="tab"`) está correctamente anunciado para usuarios de lectores de pantalla.  
Si **ninguna pestaña tiene `aria-selected="true"`**, se genera una incidencia.

## 📌 ¿Por qué es importante?
Los usuarios que navegan con el teclado o lectores de pantalla **no pueden ver visualmente qué pestaña está activa**, por lo que necesitan que el estado seleccionado sea **anunciado correctamente**.

## ⚠️ Problema Detectado
- **Las pestañas (`role="tab"`) deben indicar cuál está activa** con `aria-selected="true"`.
- **Si falta este atributo**, el usuario no sabrá qué pestaña está seleccionada.

### ❌ **Ejemplo Incorrecto**
```html
<div role="tablist">
    <button role="tab">Home</button>
    <button role="tab">Deals</button>
    <button role="tab" class="active">My Groupons</button> <!-- ❌ Falta aria-selected="true" -->
</div>
✅ Ejemplo Correcto
html
Copy
Edit
<div role="tablist">
    <button role="tab" aria-selected="false">Home</button>
    <button role="tab" aria-selected="false">Deals</button>
    <button role="tab" aria-selected="true">My Groupons</button> <!-- ✅ Se anuncia correctamente -->
</div>
⚡ Instalación
Asegúrate de tener BeautifulSoup instalado:

bash
Copy
Edit
pip install beautifulsoup4
🚀 Uso del Tester
python
Copy
Edit
from check_tab_aria_selected import check_tab_aria_selected

with open("test_tab_aria_selected.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "https://example.com"
incidencias = check_tab_aria_selected(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si ninguna pestaña tiene aria-selected="true", el tester reportará:

json
Copy
Edit
{
    "title": "Selected tab state is not announced",
    "type": "Screen Reader",
    "severity": "Medium",
    "description": "Ninguna de las pestañas en la página tiene el atributo `aria-selected=\"true\"`. Esto significa que los usuarios con lectores de pantalla no sabrán cuál pestaña está activa.",
    "remediation": "Añadir `aria-selected=\"true\"` a la pestaña activa dentro de un `role=\"tablist\"`. Ejemplo: `<button role=\"tab\" aria-selected=\"true\">My Groupons</button>`.",
    "wcag_reference": "4.1.2",
    "impact": "Los usuarios con lectores de pantalla podrían no saber cuál pestaña está seleccionada.",
    "page_url": "https://example.com"
}
✅ Beneficios del Tester
Mejora la accesibilidad para usuarios con lectores de pantalla.
Detecta automáticamente si falta aria-selected="true" en pestañas activas.
Puede ejecutarse de forma independiente o integrarse en global_tester.py.
💡 ¡Con este tester, garantizas una mejor experiencia accesible en tus pestañas! 🚀

yaml
Copy
Edit

---

### **📌 ¿Qué incluye este README?**
✅ **Explica el propósito del tester y por qué es importante.**  
✅ **Muestra ejemplos claros de código incorrecto y correcto.**  
✅ **Explica cómo instalarlo y ejecutarlo.**  
✅ **Incluye un ejemplo JSON de una incidencia real.**  
✅ **Resume los beneficios del tester.**  

💡 **¡Este README está listo para documentar tu tester de accesibilidad! 🚀**