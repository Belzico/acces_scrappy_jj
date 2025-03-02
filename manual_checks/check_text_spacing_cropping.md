# **Tester de Contenido Recortado con Espaciado de Texto (check_text_spacing_cropping.py)**

Este tester analiza el contenido HTML para detectar si el texto queda **recortado** al aplicar espaciados de texto accesibles (WCAG 1.4.12). Identifica elementos con **overflow: hidden** (en sus variantes), alturas fijas en píxeles y otras configuraciones que pueden ocultar contenido cuando se incrementan line-height, word-spacing, letter-spacing, etc.

---

## **¿Por qué es importante?**

- **WCAG 1.4.12 – Text Spacing** establece que los usuarios deben poder **ajustar el espaciado de texto** (líneas, palabras, letras y párrafos) sin que el contenido se solape o se recorte.
- **Usuarios con discapacidades visuales, cognitivas o de lectura** a menudo personalizan el espaciado para leer con mayor comodidad.
- Cualquier contenedor que limite la expansión del texto (por ejemplo, con `overflow: hidden;` o `height: 100px;`) puede provocar que parte del contenido quede inaccesible.

---

## **¿Qué hace este tester?**
1. **Busca estilos inline** (`style="..."`) en contenedores de texto (`<p>`, `<div>`, `<span>`, `<section>`, `<article>`).
2. **Usa expresiones regulares** para detectar:
   - `overflow: hidden;`, `overflow-x: hidden;` o `overflow-y: hidden;`
   - `height: Npx;` o `max-height: Npx;`
3. **Genera incidencias** si halla configuraciones problemáticas:
   - **"Content may be cropped with text spacing adjustments"** cuando `overflow: hidden;`.
   - **"Fixed height detected, may crop text"** cuando hay una altura fija en píxeles.

---

## **Ejemplo de Incidencia**
```json
{
  "title": "Content may be cropped with text spacing adjustments",
  "type": "Zoom",
  "severity": "High",
  "description": "Se detectó `overflow: hidden;` en un contenedor de texto. Esto puede hacer que el contenido se recorte al aumentar el espaciado.",
  "remediation": "Evitar `overflow: hidden;` en contenedores de texto. Permitir que el contenido se expanda correctamente.",
  "wcag_reference": "1.4.12",
  "impact": "Usuarios que necesiten espaciado adicional podrían no ver todo el contenido.",
  "page_url": "test_page.html"
}
Uso y Ejemplo
Integrarlo en global_tester.py para ejecutarlo automáticamente.
Probarlo manualmente:
python
Copy
Edit
with open("test_spacing.html", "r", encoding="utf-8") as f:
    html_content = f.read()

incidences = check_text_spacing_cropping(html_content, "test_spacing.html")
for inc in incidences:
    print(inc)
HTML de Prueba con Error
html
Copy
Edit
<div style="OVERFLOW-x: hidden; height: 100px;">
  <p>Este texto podría cortarse cuando se aplique un mayor espaciado de líneas, letras o palabras.</p>
</div>
Resultado esperado: Se reportará una incidencia por overflow: hidden; y height: 100px;.

Solución Recomendada
Evitar overflow: hidden; en contenedores de texto crítico.
Usar height: auto; o min-height: auto; en lugar de valores fijos en píxeles.
Permitir que el contenedor se ajuste al aumentar line-height, letter-spacing, word-spacing, etc.
Verificar que no se oculte el contenido mediante overflow-x: hidden; o overflow-y: hidden;.
Referencias
WCAG 1.4.12 (Text Spacing):
https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html
Mejorando Accesibilidad con Espaciados:
https://www.w3.org/WAI/tutorials/page-structure/styling/
Este tester garantiza que al personalizar el espaciado de texto, el contenido siga completamente visible y sin recortes, cumpliendo con WCAG 1.4.12.