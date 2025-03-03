📌 README.md
md
Copy
Edit
# 🔍 Buttons/Links Identified Only by Color - `check_buttons_only_by_color.py`

Este script detecta **botones y enlaces que solo se identifican por su color**, sin pistas visuales adicionales como subrayado, borde o icono.  
Si un usuario **no puede diferenciar colores fácilmente**, es posible que no reconozca estos elementos como interactivos.

## 📌 ¿Por qué es importante?
Según las **Directrices de Accesibilidad para el Contenido Web (WCAG)**, el color no debe ser la única pista para identificar un elemento interactivo.  
Si un enlace o botón solo cambia de color sin otra indicación visual, puede generar problemas como:

- ❌ **Dificultad para usuarios con daltonismo o baja visión.**
- ❌ **Falta de contraste suficiente con el texto circundante.**
- ❌ **Dificultad para interactuar con los botones/enlaces.**

---

## ⚠️ **Problema Detectado**
El script busca elementos `<button>` y `<a>` que **solo usan color para diferenciarse** del texto normal.  
Ejemplo de código problemático:

### ❌ **Ejemplo Incorrecto (Con Error)**
```html
<a href="#" style="color: #0067A0;">Learn more</a>
<button style="color: #0067A0;">Continuar</button>
✅ Ejemplo Correcto (Solucionado)
html
Copy
Edit
<a href="#" style="color: #0067A0; text-decoration: underline; font-weight: bold;">Learn more</a>
<button style="color: #0067A0; border: 2px solid #0067A0; background-color: #f0f0f0;">Continuar</button>
🚀 Cómo Usar el Tester
📌 Instalación
Asegúrate de tener BeautifulSoup instalado:

bash
Copy
Edit
pip install beautifulsoup4
📌 Ejecutar el Tester en un Archivo HTML
python
Copy
Edit
from check_buttons_only_by_color import check_buttons_only_by_color

with open("test_buttons_only_by_color_error.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///ruta/del/archivo/test_buttons_only_by_color_error.html"
incidencias = check_buttons_only_by_color(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si hay botones/enlaces sin pista visual adicional, el tester reportará:

json
Copy
Edit
{
    "title": "Multiple buttons/links identified only by use of color",
    "type": "Color",
    "severity": "Low",
    "description": "Algunos botones o enlaces solo se identifican por su color sin pistas visuales adicionales. Los usuarios con discapacidad visual pueden no reconocerlos correctamente.",
    "remediation": "Añadir pistas visuales como `text-decoration: underline` en enlaces, `border` en botones o negrita en el texto para diferenciarlos del contenido normal.",
    "wcag_reference": "1.4.1",
    "impact": "Los usuarios que no perciben bien los colores pueden no notar que estos elementos son interactivos.",
    "page_url": "file:///ruta/del/archivo/test_buttons_only_by_color_error.html",
    "affected_elements": [
        "<a href=\"#\" style=\"color: #0067A0;\">Learn more</a>",
        "<button style=\"color: #0067A0;\">Continuar</button>"
    ]
}
✅ Beneficios del Tester
✔ Detecta botones y enlaces identificados solo por color.
✔ Muestra los elementos afectados y su código.
✔ Mejora la accesibilidad para usuarios con dificultades visuales.
✔ Fácil integración en global_tester.py.

💡 ¡Con este tester garantizamos que todos los botones y enlaces sean accesibles! 🚀