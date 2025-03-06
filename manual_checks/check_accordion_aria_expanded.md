📌 README.md
md
Copy
Edit
# 🔍 Accordion Accessibility Checker

Este script verifica si los **botones de acordeón** (`accordion-toggle`) tienen el atributo `aria-expanded` correctamente configurado.  
Si **ningún botón de acordeón tiene `aria-expanded="true"` o `aria-expanded="false"`**, se genera una incidencia.

## 📌 ¿Por qué es importante?
Los usuarios que navegan con el teclado o lectores de pantalla **no pueden ver visualmente si un acordeón está abierto o cerrado**, por lo que necesitan que el estado expandido sea **anunciado correctamente**.

## ⚠️ Problema Detectado
- **Los botones de acordeón deben indicar su estado con `aria-expanded="true"` o `aria-expanded="false"`**.
- **Si falta este atributo**, el usuario no sabrá si hay contenido expandible disponible.
- **Se recomienda usar `<button>` en lugar de `<a>` para controlar los acordeones**.

### ❌ **Ejemplo Incorrecto**
```html
<button class="accordion-toggle">Sección 1</button> <!-- ❌ Falta aria-expanded -->
<div class="accordion-content">Contenido de la sección 1</div>
✅ Ejemplo Correcto
html
Copy
Edit
<button class="accordion-toggle" aria-expanded="false">Sección 1</button> <!-- ✅ Se anuncia correctamente -->
<div class="accordion-content" hidden>Contenido de la sección 1</div>
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
from check_accordion_aria_expanded import check_accordion_aria_expanded

with open("test_accordion_aria_expanded.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "https://example.com"
incidencias = check_accordion_aria_expanded(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si ningún acordeón tiene aria-expanded, el tester reportará:

json
Copy
Edit
{
    "title": "Accordion items don’t announce state",
    "type": "Screen Reader",
    "severity": "Medium",
    "description": "Uno o más botones de acordeón no tienen el atributo `aria-expanded`. Esto significa que los usuarios con lectores de pantalla no sabrán si el acordeón está expandido o colapsado.",
    "remediation": "Añadir `aria-expanded=\"true\"` o `aria-expanded=\"false\"` al botón de acordeón. Ejemplo: `<button aria-expanded=\"false\">Sección 1</button>`.",
    "wcag_reference": "4.1.2",
    "impact": "Los usuarios con lectores de pantalla podrían no saber que hay contenido expandible en la página.",
    "page_url": "https://example.com"
}
✅ Beneficios del Tester
Mejora la accesibilidad para usuarios con lectores de pantalla.
Detecta automáticamente si falta aria-expanded en botones de acordeón.
Puede ejecutarse de forma independiente o integrarse en global_tester.py.
💡 ¡Con este tester, garantizas una mejor experiencia accesible en acordeones interactivos! 🚀