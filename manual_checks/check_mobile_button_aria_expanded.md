📌 README.md
md
Copy
Edit
# 🔍 Mobile Button Accessibility Checker

Este script verifica si los **botones expandibles** en dispositivos móviles tienen el atributo `aria-expanded` correctamente configurado.  
Si **ningún botón expandible tiene `aria-expanded="true"` o `aria-expanded="false"`**, se genera una incidencia.

## 📌 ¿Por qué es importante?
Los usuarios que navegan con el teclado o lectores de pantalla **no pueden ver visualmente si un botón ha expandido su contenido**, por lo que necesitan que el estado expandido/colapsado sea **anunciado correctamente**.

## ⚠️ Problema Detectado
- **Los botones expandibles deben indicar su estado con `aria-expanded="true"` o `aria-expanded="false"`**.
- **Si falta este atributo**, el usuario no sabrá si hay contenido visible o colapsado.
- **Al hacer doble tap en el botón, el lector de pantalla debería anunciar el cambio de estado.**

### ❌ **Ejemplo Incorrecto**
```html
<button>Ver más</button> <!-- ❌ Falta aria-expanded -->
<div role="button">Mostrar información</div> <!-- ❌ Falta aria-expanded -->
<span role="button" aria-expanded="">Opciones</span> <!-- ❌ Estado incorrecto -->
<a href="#" role="button" class="expandable">Ubicación</a> <!-- ❌ Sin aria-expanded -->
✅ Ejemplo Correcto
html
Copy
Edit
<button aria-expanded="false">Ver más</button> <!-- ✅ Correcto -->
<div role="button" aria-expanded="true">Mostrar información</div> <!-- ✅ Correcto -->
<span role="button" aria-expanded="false">Opciones</span> <!-- ✅ Correcto -->
<a href="#" role="button" aria-expanded="true">Ubicación</a> <!-- ✅ Correcto -->
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
from check_mobile_button_aria_expanded import check_mobile_button_aria_expanded

with open("test_mobile_button_aria_expanded.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "https://example.com"
incidencias = check_mobile_button_aria_expanded(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si ningún botón expandible tiene aria-expanded, el tester reportará:

json
Copy
Edit
{
    "title": "Button has no expanded/collapsed state announced on mobile",
    "type": "Screen Readers",
    "severity": "Medium",
    "description": "Uno o más botones con estados expandibles no tienen el atributo `aria-expanded`. Esto significa que los usuarios con lectores de pantalla en dispositivos móviles no sabrán si el botón está expandido o colapsado.",
    "remediation": "Añadir `aria-expanded=\"true\"` o `aria-expanded=\"false\"` al botón expandible. Ejemplo: `<button aria-expanded=\"false\">Ver más</button>`.",
    "wcag_reference": "4.1.2",
    "impact": "Los usuarios con lectores de pantalla en dispositivos móviles no recibirán información sobre el estado del botón.",
    "page_url": "https://example.com"
}
✅ Beneficios del Tester
Mejora la accesibilidad para usuarios con lectores de pantalla en dispositivos móviles.
Detecta automáticamente si falta aria-expanded en botones expandibles.
Puede ejecutarse de forma independiente o integrarse en global_tester.py.
💡 ¡Con este tester, garantizas una mejor experiencia accesible en botones expandibles en móviles! 🚀