📌 README.md
md
Copy
Edit
# 🔍 Page Language Mismatch Checker

Este script verifica si el contenido visible de una página coincide con el idioma declarado en `<html lang="xx">`.  
Si más del **20% del contenido** está en un idioma diferente, se genera una incidencia.  

## 📌 ¿Cómo funciona?
1. **Extrae todo el texto visible de la página**, ignorando scripts, estilos y metadatos.
2. **Detecta el idioma de cada fragmento de texto** usando `langid` (basado en fastText, más preciso que `langdetect`).
3. **Cuenta cuántos fragmentos están en cada idioma**.
4. **Si más del 20% del contenido no coincide con `<html lang>`**, se genera una alerta.

## ⚡ Instalación
Asegúrate de tener `BeautifulSoup` y `langid` instalados:
```bash
pip install beautifulsoup4 langid
🚀 Uso
python
Copy
Edit
from check_page_language_mismatch import check_page_language_mismatch

with open("test_page.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "https://example.com"
incidencias = check_page_language_mismatch(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia
json
Copy
Edit
{
    "title": "Page language mismatch",
    "type": "Other A11y",
    "severity": "High",
    "description": "Se detectó que el 40.0% del contenido visible de la página está en un idioma diferente a 'es' definido en <html lang>.",
    "remediation": "Asegurar que al menos el 80% del contenido visible coincida con el idioma declarado en <html lang>.",
    "wcag_reference": "3.1.1",
    "impact": "Los usuarios con lectores de pantalla podrían recibir una pronunciación incorrecta si el contenido está en un idioma diferente al definido en la página.",
    "page_url": "https://example.com"
}
✅ Beneficios
Evita errores en páginas multiidioma.
Mayor precisión con langid en textos cortos.
Solo genera alertas si el desajuste es significativo (+20%).
💡 ¡Mejora la accesibilidad web y asegura que los idiomas coincidan correctamente! 🚀