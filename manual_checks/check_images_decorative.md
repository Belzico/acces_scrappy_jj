# 🏷️ `check_images_decorative.py` - Evaluador de Imágenes y Elementos Decorativos

## 📌 Descripción

Este script analiza un documento HTML en busca de **imágenes y elementos decorativos** mal configurados que puedan afectar la accesibilidad.  
Verifica si las imágenes están correctamente marcadas como decorativas (`alt=""`), si los separadores (`<hr>`, `<svg>`) están ocultos y si las imágenes innecesariamente reciben foco o son anunciadas por los lectores de pantalla.

📚 **Referencias oficiales**:
- **WCAG 2.1 - 1.1.1:** [Non-text Content](https://www.w3.org/WAI/WCAG21/quickref/#non-text-content)
- **W3C Decorative Images Guide:** [https://www.w3.org/WAI/tutorials/images/decorative/](https://www.w3.org/WAI/tutorials/images/decorative/)

---

## 🔍 **Errores detectados**

### **1️⃣ Imágenes sin `alt` (Error crítico)**
🔴 **Problema:**  
Las imágenes sin `alt` son inaccesibles para los lectores de pantalla, lo que afecta la usabilidad.

✅ **Solución:**  
- Si la imagen es decorativa, **usar `alt=""` y `aria-hidden="true"`**.
- Si la imagen es informativa, **describir su contenido en el `alt`**.

📌 **Ejemplo incorrecto:**
```html
<img src="banner.jpg">
📌 Ejemplo corregido:

html
Copy
Edit
<img src="banner.jpg" alt="">
2️⃣ Imágenes decorativas que reciben foco o son anunciadas
🔴 Problema:
Las imágenes marcadas como decorativas (alt="") no deben ser anunciadas ni recibir foco en el teclado.

✅ Solución:

Agregar aria-hidden="true" o role="presentation" para ocultarlas a tecnologías asistivas.
Evitar que sean seleccionables con el teclado (tabindex="-1").
📌 Ejemplo incorrecto:

html
Copy
Edit
<img src="background.jpg" alt="" tabindex="0">
📌 Ejemplo corregido:

html
Copy
Edit
<img src="background.jpg" alt="" aria-hidden="true" tabindex="-1">
3️⃣ Imágenes decorativas con alt incorrecto
🔴 Problema:
Si una imagen es puramente decorativa, no debe tener un texto en el alt.

✅ Solución:

Usar alt="" para indicar que la imagen no es informativa.
📌 Ejemplo incorrecto:

html
Copy
Edit
<img src="decorative-pattern.jpg" alt="Decorative background pattern">
📌 Ejemplo corregido:

html
Copy
Edit
<img src="decorative-pattern.jpg" alt="">
4️⃣ Separadores (<hr>, <svg>) visibles para lectores de pantalla
🔴 Problema:
Los elementos decorativos como <hr> y <svg> no deben ser anunciados ni recibir foco.

✅ Solución:

Agregar aria-hidden="true" o role="presentation".
📌 Ejemplo incorrecto:

html
Copy
Edit
<hr>
<svg><circle cx="50" cy="50" r="40"></circle></svg>
📌 Ejemplo corregido:

html
Copy
Edit
<hr aria-hidden="true">
<svg aria-hidden="true"><circle cx="50" cy="50" r="40"></circle></svg>
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
from manual_checks.check_images_decorative import check_images_decorative

html_test = """
<!DOCTYPE html>
<html>
<body>
    <h1>Ejemplo de imágenes decorativas</h1>
    
    <!-- Imagen sin alt -->
    <img src="missing-alt.jpg">
    
    <!-- Imagen decorativa con alt incorrecto -->
    <img src="decorative-pattern.jpg" alt="Decorative background pattern">
    
    <!-- Imagen decorativa que recibe foco -->
    <img src="background.jpg" alt="" tabindex="0">
    
    <!-- Separador sin aria-hidden -->
    <hr>
</body>
</html>
"""

errors = check_images_decorative(html_test, "https://example.com")

for err in errors:
    print(f"🔴 {err['title']}")
    print(f"📌 {err['description']}")
    print(f"🛠 Solución sugerida: {err['remediation']}\n")
🛠 Salida esperada en consola
pgsql
Copy
Edit
🔴 Missing alt attribute
📌 The image 'missing-alt.jpg' does not have an 'alt' attribute.
🛠 Solución sugerida: Use alt="" for decorative images or provide a meaningful description.

🔴 Decorative image has incorrect alt
📌 The image 'decorative-pattern.jpg' is likely decorative but has an alt text.
🛠 Solución sugerida: Use alt="" to indicate that this image is purely decorative.

🔴 Decorative image is focused and announced
📌 The image 'background.jpg' is decorative but is focusable.
🛠 Solución sugerida: Add aria-hidden="true" or role="presentation" and set tabindex="-1".

🔴 Decorative separator is focused and announced
📌 A decorative element ('hr') is visible to screen readers but should be hidden.
🛠 Solución sugerida: Add aria-hidden="true" or role="presentation" to this element.
📌 Resumen
✅ Este tester evalúa accesibilidad en imágenes y elementos decorativos en HTML:

🚨 Errores críticos: alt faltante o mal usado en imágenes decorativas.
🛠 Revisión de separadores: <hr> y <svg> sin aria-hidden="true".
📖 Cumple con WCAG 2.1: Mejora la navegación con lectores de pantalla.
🔥 Ideal para garantizar una experiencia accesible en la web! 🚀