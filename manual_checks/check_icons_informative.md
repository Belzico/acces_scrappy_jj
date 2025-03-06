# 🏷️ `check_icons_informative.py` - Evaluador de Íconos Informativos Accesibles

## 📌 Descripción

Este script evalúa si los íconos (CSS, imágenes y SVGs) utilizados en un documento HTML **son accesibles para los lectores de pantalla**.  
Detecta íconos sin etiquetas accesibles, imágenes informativas sin `alt` y SVGs sin elementos accesibles.

Se basa en las recomendaciones de **W3C para accesibilidad en imágenes e íconos**.

📚 **Referencias oficiales**:
- **WCAG 2.1 - 1.1.1:** [Non-text Content](https://www.w3.org/WAI/WCAG21/quickref/#non-text-content)
- **W3C Images & Icons Accessibility Guide:** [https://www.w3.org/WAI/tutorials/images/](https://www.w3.org/WAI/tutorials/images/)

---

## 🔍 **Errores detectados**

### **1️⃣ Íconos CSS sin texto accesible**
🔴 **Problema:**  
Los íconos agregados con clases de CSS (`<span>`, `<i>`) pueden ser **invisibles para los lectores de pantalla** si no tienen un `aria-label` o un texto alternativo.

✅ **Solución:**  
- Agregar `aria-label` o `aria-labelledby` con un valor descriptivo.  
- O incluir un texto oculto con CSS (`.sr-only`).

📌 **Ejemplo incorrecto:**
```html
<span class="icon active"></span>
📌 Ejemplo corregido:

html
Copy
Edit
<span class="icon active" aria-label="Active"></span>
2️⃣ Imágenes informativas sin alt
🔴 Problema:
Si una imagen transmite información y no tiene un alt, los usuarios de lectores de pantalla no podrán interpretarla.

✅ Solución:

Agregar un alt descriptivo que explique la información que transmite la imagen.
📌 Ejemplo incorrecto:

html
Copy
Edit
<img src="warning.png">
📌 Ejemplo corregido:

html
Copy
Edit
<img src="warning.png" alt="Warning: Invalid credentials">
3️⃣ SVGs informativos sin title o aria-labelledby
🔴 Problema:
Los SVGs informativos sin title o aria-labelledby no son identificados correctamente por los lectores de pantalla.

✅ Solución:

Agregar un <title> dentro del <svg>.
O utilizar aria-labelledby apuntando a un <title> existente.
📌 Ejemplo incorrecto:

html
Copy
Edit

📌 Ejemplo corregido:

html
Copy
Edit

⚙️ Instalación
Este script requiere Python 3.7+ y BeautifulSoup4:

bash
Copy
Edit
pip install beautifulsoup4
🚀 Cómo usar este tester
Ejecuta el script pasando un documento HTML como entrada:

python
Copy
Edit
from manual_checks.check_icons_informative import check_icons_informative

html_test = """
<!DOCTYPE html>
<html>
<body>
    <h1>Ejemplo de íconos e imágenes</h1>
    
    <!-- Ícono sin etiqueta accesible -->
    <span class="icon active"></span>
    
    <!-- Imagen informativa sin alt -->
    <img src="warning.png">

    <!-- SVG sin título accesible -->
    <svg viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40"></circle>
    </svg>
</body>
</html>
"""

errors = check_icons_informative(html_test, "https://example.com")

for err in errors:
    print(f"🔴 {err['title']}")
    print(f"📌 {err['description']}")
    print(f"🛠 Solución sugerida: {err['remediation']}\n")
🛠 Salida esperada en consola
swift
Copy
Edit
🔴 Informative icon is not announced
📌 An informative icon is present but does not provide an accessible label.
🛠 Solución sugerida: Use aria-label="Active" o agregue un texto accesible oculto con CSS.

🔴 Informative image is not set as such
📌 An image that conveys information does not have an alternative text (`alt`).
🛠 Solución sugerida: Agregue un alt="Warning: Invalid credentials".

🔴 Informative SVG is not accessible
📌 An SVG that conveys information does not have a `title` element or `aria-labelledby`.
🛠 Solución sugerida: Agregue <title> dentro del SVG o use aria-labelledby.
📌 Resumen
✅ Este tester evalúa accesibilidad en íconos e imágenes informativas en HTML:

🚨 Errores críticos: íconos y SVGs sin etiquetas accesibles.
🛠 Revisión de imágenes: imágenes sin alt se marcan como error.
📖 Cumple con WCAG 2.1: Garantiza accesibilidad para usuarios con discapacidad visual.
🔥 Ideal para mejorar accesibilidad en aplicaciones web! 🚀

Copy
Edit
