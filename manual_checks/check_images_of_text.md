check_images_of_text.py - Verificación de imágenes de texto con OCR
🔍 Descripción
Este script analiza imágenes en un documento HTML para detectar si contienen texto incrustado y verifica si dicho texto tiene una alternativa textual adecuada en el contenido HTML.

¿Cómo funciona?

Extrae todas las imágenes (<img>) del HTML.
Verifica si la imagen existe en la carpeta downloaded_images.
Ejecuta OCR con pytesseract para extraer el texto contenido en la imagen.
Compara el texto extraído con el alt de la imagen y el contenido cercano en el HTML.
Genera incidencias si el texto en la imagen no tiene una versión textual adecuada en la página.
Este análisis sigue las pautas de WCAG 2.1 y la técnica C30 de W3C para imágenes de texto:
🔗 WCAG 1.4.5 - Imágenes de Texto
🔗 Técnica C30 - Uso de CSS en lugar de imágenes de texto

🛠️ Requisitos
Antes de ejecutar este script, asegúrate de tener instalados los siguientes paquetes:

bash
Copy
Edit
pip install beautifulsoup4 pillow pytesseract
Además, debes tener Tesseract OCR instalado en tu sistema:
🔗 Tesseract OCR - Descarga

⚠️ IMPORTANTE: En Windows, configura la ruta de tesseract.exe en tu código:

python
Copy
Edit
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
📄 Cómo probar este tester
1️⃣ Generar una imagen con texto
Si deseas probar el OCR, genera una imagen con texto usando este código:

python
Copy
Edit
from PIL import Image, ImageDraw, ImageFont

def create_text_image(text, filename="downloaded_images/sample_image.png"):
    image_size = (400, 100)  
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    text_position = (10, 40)
    draw.text(text_position, text, fill="black", font=font)

    image.save(filename)
    print(f"✅ Imagen guardada en: {filename}")

create_text_image("Oferta especial")
2️⃣ Crear un HTML de prueba
Guarda este HTML como test.html en la misma carpeta:

html
Copy
Edit
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prueba de Imagen de Texto</title>
</head>
<body>
    <h1>Oferta especial</h1>
    <p>Aprovecha nuestra gran promoción.</p>
    <img src="downloaded_images/sample_image.png" alt="Descuento increíble">
</body>
</html>
3️⃣ Ejecutar el tester
Carga el contenido HTML y ejecuta el script:

python
Copy
Edit
import os

# Leer el HTML de prueba
with open("test.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# URL ficticia
page_url = "file://test.html"

# Ejecutar la prueba
results = check_images_of_text(html_content, page_url)

# Mostrar resultados
for result in results:
    print(f"🔴 {result['title']}: {result['description']}")
🚨 Posibles errores detectados
Error	Descripción
Imagen con texto sin alternativa	La imagen contiene texto (detectado por OCR), pero no hay una versión textual equivalente en el HTML.
Texto en imagen y alt incorrecto	El texto en la imagen no coincide con el alt proporcionado.
OCR falló	No se pudo extraer el texto de la imagen (posible problema con Tesseract).
📚 Referencias
🔗 WCAG 1.4.5 - Imágenes de Texto
🔗 Técnica C30 - Uso de CSS en lugar de imágenes de texto
🔗 Tesseract OCR
✅ Conclusión
Este tester ayuda a detectar imágenes que contienen texto y alerta si no hay una alternativa textual adecuada en el HTML. Esto mejora la accesibilidad y asegura el cumplimiento de WCAG 2.1.

Si el análisis detecta problemas, considera reemplazar la imagen con texto real en HTML o implementar la Técnica C30 para permitir la conmutación entre imágenes y texto. 🚀