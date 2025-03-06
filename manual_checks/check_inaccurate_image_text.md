# 🏷️ `check_informative_images.py` - Evaluador de Imágenes Informativas y su Texto Alternativo

## 📌 Descripción

Este script analiza un documento HTML para detectar **imágenes informativas mal configuradas** y **compara su texto alternativo (`alt`) con el texto real de la imagen mediante OCR**.  
Verifica que las imágenes tengan un `alt` descriptivo y que no sean genéricas o incorrectas.

📚 **Referencias oficiales**:
- **WCAG 2.1 - 1.1.1:** [Non-text Content](https://www.w3.org/WAI/WCAG21/quickref/#non-text-content)
- **W3C Informative Images Guide:** [https://www.w3.org/WAI/tutorials/images/informative/](https://www.w3.org/WAI/tutorials/images/informative/)

---

## 🔍 **Errores detectados**

### **1️⃣ Imágenes informativas sin `alt` (Error crítico)**
🔴 **Problema:**  
Las imágenes que contienen información visual **deben tener un `alt` descriptivo** para que los lectores de pantalla puedan interpretarlas.

✅ **Solución:**  
- Agregar un `alt` que describa la información clave de la imagen.

📌 **Ejemplo incorrecto:**
```html
<img src="instructions.png">
📌 Ejemplo corregido:

html
Copy
Edit
<img src="instructions.png" alt="Push the cap down and turn it counter-clockwise.">
2️⃣ Imágenes con alt genérico
🔴 Problema:
Los textos alternativos como "image", "photo", "icon" no proporcionan información útil a los lectores de pantalla.

✅ Solución:

Reemplazar el alt genérico por una descripción clara del contenido visual.
📌 Ejemplo incorrecto:

html
Copy
Edit
<img src="dog.jpg" alt="Photo">
📌 Ejemplo corregido:

html
Copy
Edit
<img src="dog.jpg" alt="Dog with a bell attached to its collar.">
3️⃣ Comparación con OCR: alt no coincide con el texto en la imagen
🔴 Problema:
Si una imagen contiene texto, el alt debe reflejar su contenido de manera precisa.

✅ Solución:

Utilizar OCR para extraer el texto de la imagen y comparar con el alt.
📌 Ejemplo incorrecto (OCR detecta texto diferente al alt)

html
Copy
Edit
<img src="banner.jpg" alt="Special offer">
📌 Texto detectado en la imagen por OCR:

pgsql
Copy
Edit
Get 50% off on all summer products!
📌 Ejemplo corregido:

html
Copy
Edit
<img src="banner.jpg" alt="Get 50% off on all summer products!">
⚙️ Instalación
Este script requiere Python 3.7+, BeautifulSoup4, pytesseract y Pillow:

bash
Copy
Edit
pip install beautifulsoup4 pytesseract pillow
Además, debes instalar Tesseract OCR y configurarlo en tu sistema:

Windows: Descarga e instala desde https://github.com/UB-Mannheim/tesseract/wiki.
Luego, configura la ruta en el script:

python
Copy
Edit
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
Linux/macOS:

bash
Copy
Edit
sudo apt install tesseract-ocr  # Ubuntu/Debian
brew install tesseract          # macOS (Homebrew)
🚀 Cómo usar este tester
Ejecuta el script pasando un documento HTML como entrada:

python
Copy
Edit
from manual_checks.check_informative_images import check_informative_images

html_test = """
<!DOCTYPE html>
<html>
<body>
    <h1>Ejemplo de imágenes informativas</h1>
    
    <!-- Imagen sin alt -->
    <img src="missing-alt.jpg">
    
    <!-- Imagen con alt genérico -->
    <img src="warning.png" alt="Image">
    
    <!-- Imagen que contiene texto -->
    <img src="promotion.jpg" alt="Great sale">
</body>
</html>
"""

errors = check_informative_images(html_test, "https://example.com")

for err in errors:
    print(f"🔴 {err['title']}")
    print(f"📌 {err['description']}")
    print(f"🛠 Solución sugerida: {err['remediation']}\n")
🛠 Salida esperada en consola
vbnet
Copy
Edit
🔴 Informative image with missing or empty alt
📌 The image 'missing-alt.jpg' has no or empty alt.
🛠 Solución sugerida: Add a short, meaningful alt text.

🔴 Informative image has a generic alt text
📌 The image 'warning.png' uses a generic alt 'Image', which doesn't convey meaning.
🛠 Solución sugerida: Use a descriptive alt, like "Warning: Invalid credentials".

🔴 Alt text may be inaccurate compared to image text
📌 Image: 'promotion.jpg'
   OCR text: 'Limited time offer: Buy 1 get 1 free...'
   Alt: 'Great sale'
   Overlap: 15.0%
🛠 Solución sugerida: Update the alt to match the text in the image.
📌 Resumen
✅ Este tester evalúa la accesibilidad de imágenes informativas en HTML:

🚨 Errores críticos: alt ausente o genérico.
🛠 Comparación OCR: alt inexacto respecto al texto en la imagen.
📖 Cumple con WCAG 2.1: Mejora la accesibilidad para usuarios de lectores de pantalla.
🔥 Ideal para validar imágenes en aplicaciones web y mejorar la accesibilidad! 🚀

Copy
Edit
