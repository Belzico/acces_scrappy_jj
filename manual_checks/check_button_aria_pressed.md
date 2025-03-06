📌 README.md
md
Copy
Edit
# 🔍 Button Selected State Accessibility Checker

Este script verifica si el **estado seleccionado** de un botón (`role="button"`) está correctamente anunciado para usuarios de lectores de pantalla.  
Si **ningún botón tiene `aria-pressed="true"`**, se genera una incidencia.

## 📌 ¿Por qué es importante?
Los usuarios que navegan con el teclado o lectores de pantalla **no pueden ver visualmente qué botón está seleccionado**, por lo que necesitan que el estado seleccionado sea **anunciado correctamente**.

## ⚠️ Problema Detectado
- **Los botones (`role="button"`) deben indicar cuál está activo** con `aria-pressed="true"`.
- **Si falta este atributo**, el usuario no sabrá qué botón está seleccionado.

### ❌ **Ejemplo Incorrecto**
```html
<button role="button" class="active">Posición Global</button> <!-- ❌ Falta aria-pressed="true" -->
✅ Ejemplo Correcto
html
Copy
Edit
<button role="button" aria-pressed="true">Posición Global</button> <!-- ✅ Se anuncia correctamente como seleccionado -->
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
from check_button_aria_pressed import check_button_aria_pressed

with open("test_button_aria_pressed.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "https://example.com"
incidencias = check_button_aria_pressed(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si ningún botón tiene aria-pressed="true", el tester reportará:

json
Copy
Edit
{
    "title": "Visually selected button is not announced",
    "type": "Screen Reader",
    "severity": "Medium",
    "description": "Ningún botón en la página tiene el atributo `aria-pressed=\"true\"`. Esto significa que los usuarios con lectores de pantalla no sabrán qué botón está seleccionado.",
    "remediation": "Añadir `aria-pressed=\"true\"` al botón seleccionado. Ejemplo: `<button role=\"button\" aria-pressed=\"true\">Posición Global</button>`.",
    "wcag_reference": "4.1.2",
    "impact": "Los usuarios con lectores de pantalla podrían no saber cuál botón está seleccionado.",
    "page_url": "https://example.com"
}
✅ Beneficios del Tester
Mejora la accesibilidad para usuarios con lectores de pantalla.
Detecta automáticamente si falta aria-pressed="true" en botones seleccionados.
Puede ejecutarse de forma independiente o integrarse en global_tester.py.
💡 ¡Con este tester, garantizas una mejor experiencia accesible en tus botones interactivos! 🚀

yaml
Copy
Edit

---

### **📌 ¿Qué incluye este README?**
✅ **Explica el propósito del tester y su importancia.**  
✅ **Ejemplos claros de código incorrecto y correcto.**  
✅ **Instrucciones de instalación y uso.**  
✅ **Ejemplo JSON de una incidencia real.**  
✅ **Resumen de los beneficios del tester.**  

💡 **¡Este README está listo para documentar tu tester de accesibilidad! 🚀**