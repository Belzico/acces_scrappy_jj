# 🖼️ `check_alt_distinction.py` - Evaluador de Texto Alternativo en Imágenes

## 📌 Descripción

Este script analiza las imágenes en un documento HTML y **verifica si su atributo `alt` es adecuado** para garantizar accesibilidad web.  
Evalúa imágenes sin `alt`, con `alt` incorrecto o redundante, usando **procesamiento de lenguaje natural (NLP)** con `Sentence Transformers`.

📚 **Referencias oficiales**:
- **WCAG 2.1 - 1.1.1:** [Non-text Content](https://www.w3.org/WAI/WCAG21/quickref/#non-text-content)
- **W3C Images Accessibility Guide:** [https://www.w3.org/WAI/tutorials/images/](https://www.w3.org/WAI/tutorials/images/)

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
<img src="chart.png">
📌 Ejemplo corregido:

html
Copy
Edit
<img src="chart.png" alt="Gráfico de ventas del último trimestre">
2️⃣ alt="" en imágenes dentro de enlaces o botones sin otro contenido accesible
🔴 Problema:
Si una imagen con alt="" es el único contenido dentro de un <a> o <button>, el enlace/botón no tendrá una etiqueta accesible, causando confusión.

✅ Solución:

Agregar un aria-label o texto visible dentro del enlace.
📌 Ejemplo incorrecto:

html
Copy
Edit
<a href="home.html"><img src="home-icon.png" alt=""></a>
📌 Ejemplo corregido:

html
Copy
Edit
<a href="home.html" aria-label="Ir a inicio">
    <img src="home-icon.png" alt="">
</a>
3️⃣ alt redundante con el texto adyacente (Detectado con IA)
🔴 Problema:
Si el alt duplica información ya escrita cerca de la imagen, los lectores de pantalla la leerán dos veces.

🧠 Cómo lo detecta el tester:

Usa Sentence Transformers para calcular la similitud semántica entre el alt y el texto adyacente.
Si la similitud es >80% (similarity_threshold=0.8), marca el alt como redundante.
✅ Solución:

Si el alt repite el texto cercano, considerar dejarlo vacío (alt="") o modificarlo.
📌 Ejemplo incorrecto:

html
Copy
Edit
<p>Este es el logotipo de la empresa.</p>
<img src="logo.png" alt="Logotipo de la empresa">
📌 Ejemplo corregido:

html
Copy
Edit
<p>Este es el logotipo de la empresa.</p>
<img src="logo.png" alt="">
⚙️ Instalación
Este script requiere Python 3.7+ y BeautifulSoup4 + sentence-transformers:

bash
Copy
Edit
pip install beautifulsoup4 sentence-transformers
🚀 Cómo usar este tester
Ejecuta el script pasando un documento HTML como entrada:

python
Copy
Edit
from manual_checks.check_alt_distinction import check_alt_distinction

html_test = """
<!DOCTYPE html>
<html>
<body>
    <h1>Ejemplo de imágenes</h1>
    
    <!-- Imagen sin alt -->
    <img src="missing-alt.jpg">
    
    <!-- Imagen dentro de un enlace sin texto accesible -->
    <a href="home.html"><img src="home-icon.png" alt=""></a>
    
    <!-- Imagen con alt redundante -->
    <p>Logo de la empresa</p>
    <img src="logo.png" alt="Logo de la empresa">
</body>
</html>
"""

errors = check_alt_distinction(html_test, "https://example.com")

for err in errors:
    print(f"🔴 {err['title']}")
    print(f"📌 {err['description']}")
    print(f"🛠 Solución sugerida: {err['suggested_fix']}\n")
🛠 Salida esperada en consola
perl
Copy
Edit
🔴 Imagen sin atributo alt
📌 Esta imagen no tiene atributo alt. Se desconoce si es decorativa o informativa.
🛠 Solución sugerida: Agregar alt apropiado. Si es decorativa, usar alt='' y aria-hidden='true'. Si es informativa, describir su contenido en alt.

🔴 Enlace/Botón sin texto accesible
📌 La imagen tiene alt='', indicando que es decorativa, pero es el único contenido de un enlace/botón sin texto ni aria-label.
🛠 Solución sugerida: Agregar un texto accesible. Ej: aria-label='Ir a inicio' o un texto dentro del enlace.

🔴 Texto alternativo redundante (semánticamente)
📌 El texto alternativo de la imagen parece redundar con el texto cercano (similaridad semántica=0.85). Esto podría causar que usuarios de lectores de pantalla escuchen la misma información dos veces.
🛠 Solución sugerida: Si la imagen es meramente decorativa, usar alt=''. Si es informativa, use un alt que aporte información adicional y no repita lo ya dicho en el texto cercano.
📌 Resumen
✅ Este tester evalúa accesibilidad en imágenes y alt en HTML:

🚨 Errores críticos: alt faltante o mal usado en enlaces/botones.
🧠 IA para redundancia: Compara alt con texto cercano usando Sentence Transformers.
📖 Cumple con WCAG 2.1: Cumple con las mejores prácticas de accesibilidad web.
🔥 Ideal para detectar fallos antes de una auditoría de accesibilidad! 🚀