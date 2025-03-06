📌 README.md
md
Copy
Edit
# 🔍 Aria-label Misuse Detector - `check_aria_label_in_div.py`

Este script detecta **uso incorrecto del atributo `aria-label` en elementos `<div>` sin un `role` definido**.  
Si **un `<div>` tiene `aria-label` pero no tiene un `role` apropiado**, puede causar problemas en validadores HTML y tecnologías asistivas.

## 📌 ¿Por qué es importante?
El atributo **`aria-label` solo debe usarse en elementos compatibles con ARIA**, como `<button>`, `<input>`, `<span>` o `<div>` con `role`.  
Cuando un `<div>` usa `aria-label` sin un `role`, puede causar:

- ❌ **Errores en validadores HTML**.
- ❌ **Dificultades para tecnologías asistivas y lectores de pantalla**.
- ❌ **Problemas de compatibilidad futura en navegadores**.

---

## ⚠️ **Problema Detectado**
El script busca `<div>` con `aria-label` que **no tienen un `role` definido**.  
Ejemplo de código problemático:

### ❌ **Ejemplo Incorrecto (Con Error)**
```html
<div aria-label="Destino 1">Destino 1</div>
<div aria-label="Destino 2">Destino 2</div>
✅ Ejemplo Correcto (Solucionado)
html
Copy
Edit
<div role="option" aria-label="Destino 1">Destino 1</div>
<div role="option" aria-label="Destino 2">Destino 2</div>
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
from check_aria_label_in_div import check_aria_label_in_div

with open("test_aria_label_in_div_error.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///ruta/del/archivo/test_aria_label_in_div_error.html"
incidencias = check_aria_label_in_div(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si hay <div> con aria-label sin role, el tester reportará:

json
Copy
Edit
{
    "title": "Aria-label attribute incorrectly used in div elements",
    "type": "HTML Validator",
    "severity": "Low",
    "description": "El atributo `aria-label` solo debe usarse en elementos que lo soporten. Actualmente se encuentra en `<div>` sin un `role` definido, lo que no es válido.",
    "remediation": "Asegurar que los `<div>` con `aria-label` tengan un `role` apropiado, como `role=\"button\"`, `role=\"option\"`, etc. Si el `aria-label` no es necesario, usar un `<span>` o `<button>` en su lugar.",
    "wcag_reference": "4.1.2",
    "impact": "No hay impacto inmediato, pero puede causar problemas en validadores y tecnologías asistivas.",
    "page_url": "file:///ruta/del/archivo/test_aria_label_in_div_error.html",
    "affected_elements": [
        "<div aria-label=\"Destino 1\">Destino 1</div>",
        "<div aria-label=\"Destino 2\">Destino 2</div>"
    ]
}
✅ Beneficios del Tester
✔ Detecta <div> con aria-label sin role.
✔ Muestra qué elementos <div> están afectados.
✔ Mejora la compatibilidad con tecnologías asistivas y validadores HTML.
✔ Fácil integración en global_tester.py.

💡 ¡Con este tester garantizamos que aria-label se use correctamente en los elementos soportados! 🚀

yaml
Copy
Edit
