📌 README.md
md
Copy
Edit
# 🔍 Button Expanded/Collapsed State Accessibility Checker

Este script verifica si los **botones expandibles** en páginas web de escritorio tienen el atributo `aria-expanded` correctamente configurado.  
Si **ningún botón expandible tiene `aria-expanded="true"` o `aria-expanded="false"`**, se genera una incidencia.

## 📌 ¿Por qué es importante?
Los usuarios que navegan con el teclado o lectores de pantalla **no pueden ver visualmente si un botón ha expandido su contenido**, por lo que necesitan que el estado expandido/colapsado sea **anunciado correctamente**.

## ⚠️ Problema Detectado
- **Los botones expandibles deben indicar su estado con `aria-expanded="true"` o `aria-expanded="false"`**.
- **Si falta este atributo**, el usuario no sabrá si hay contenido visible o colapsado.
- **Al presionar el botón, el lector de pantalla debería anunciar el cambio de estado.**

### ❌ **Ejemplo Incorrecto**
```html
<button>Categories</button> <!-- ❌ Falta aria-expanded -->
<div role="button">Ver más opciones</div> <!-- ❌ Falta aria-expanded -->
<span role="button" aria-expanded="">Menú</span> <!-- ❌ Estado incorrecto -->
✅ Ejemplo Correcto
html
Copy
Edit
<button aria-expanded="false">Categories</button> <!-- ✅ Correcto -->
<div role="button" aria-expanded="true">Ver más opciones</div> <!-- ✅ Correcto -->
<span role="button" aria-expanded="false">Menú</span> <!-- ✅ Correcto -->
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
from check_button_aria_expanded import check_button_aria_expanded

with open("test_button_aria_expanded.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "https://example.com"
incidencias = check_button_aria_expanded(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si ningún botón expandible tiene aria-expanded, el tester reportará:

json
Copy
Edit
{
    "title": "Expanded/Collapsed state is not announced in the button",
    "type": "Screen Reader",
    "severity": "Medium",
    "description": "Uno o más botones que expanden o colapsan contenido no tienen el atributo `aria-expanded`. Esto significa que los usuarios con lectores de pantalla no sabrán si el botón está expandido o colapsado.",
    "remediation": "Añadir `aria-expanded=\"true\"` o `aria-expanded=\"false\"` al botón expandible. Ejemplo: `<button aria-expanded=\"false\">Categories</button>`.",
    "wcag_reference": "4.1.2",
    "impact": "Los usuarios con lectores de pantalla no recibirán información sobre el estado del botón.",
    "page_url": "https://example.com"
}
✅ Beneficios del Tester
Mejora la accesibilidad para usuarios con lectores de pantalla en escritorio.
Detecta automáticamente si falta aria-expanded en botones expandibles.
Puede ejecutarse de forma independiente o integrarse en global_tester.py.
📌 Diferencias con check_mobile_button_aria_expanded.py
Este tester está diseñado para entornos de escritorio como JAWS + Chrome, mientras que check_mobile_button_aria_expanded.py está optimizado para dispositivos móviles con VoiceOver (iOS) y TalkBack (Android).

Tester	Dispositivo	Contexto
check_button_aria_expanded.py	🖥️ Escritorio	Menús desplegables, listas de categorías
check_mobile_button_aria_expanded.py	📱 Móviles	Botones de navegación móvil, menús de ubicación
Ambos testers pueden coexistir, ya que abordan diferentes problemas de accesibilidad.

💡 ¡Con este tester, garantizas una mejor experiencia accesible en botones expandibles en escritorio! 🚀