Aquí tienes el archivo README.md actualizado para el tester check_combobox_aria_expanded.py:

md
Copy
Edit
# 🔍 Combobox ARIA Expanded - `check_combobox_aria_expanded.py`

Este script verifica si los **comboboxes de búsqueda** tienen correctamente configurado el atributo `aria-expanded`.  
Detecta si el estado expandido/colapsado se **actualiza dinámicamente** cuando se interactúa con el combobox.

## 📌 ¿Por qué es importante?
Según **WCAG 4.1.2 (Name, Role, Value)**, los elementos interactivos deben comunicar correctamente su estado a los **lectores de pantalla**.  
Si `aria-expanded` no cambia adecuadamente, **los usuarios con discapacidad visual podrían no saber** si el menú desplegable de búsqueda está abierto o cerrado.

---

## ⚠️ **Problema Detectado**
El script busca **inputs, divs y selects** con `role="combobox"` o `aria-expanded`.  
Si `aria-expanded` **no cambia entre `true` y `false` correctamente**, se genera una incidencia.

### ❌ **Ejemplo Incorrecto (Con Error)**
```html
<input type="text" role="combobox">
🔴 Falta aria-expanded, por lo que un usuario con lector de pantalla no sabrá si la búsqueda está desplegada o colapsada.

✅ Ejemplo Correcto (Solucionado)
html
Copy
Edit
<input type="text" role="combobox" aria-expanded="false">
🟢 Solución:
✔ Añadir aria-expanded="false" cuando el menú está colapsado.
✔ Cambiar a aria-expanded="true" cuando el menú se expande.

🚀 Cómo Usar el Tester
📌 Instalación
Asegúrate de tener BeautifulSoup instalado:

sh
Copy
Edit
pip install beautifulsoup4
📌 Ejecutar el Tester en un Archivo HTML
python
Copy
Edit
from check_combobox_aria_expanded import check_combobox_aria_expanded

with open("test_combobox.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///ruta/del/archivo/test_combobox.html"
incidences = check_combobox_aria_expanded(html_content, page_url)

for inc in incidences:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si un combobox de búsqueda no cambia correctamente su aria-expanded, se genera una incidencia como esta:

json
Copy
Edit
{
    "title": "Search combobox missing aria-expanded",
    "type": "Screen Reader",
    "severity": "Medium",
    "description": "One or more search comboboxes do not properly update the `aria-expanded` attribute. When the search menu expands, `aria-expanded` should change to `true`, and when collapsed, it should change to `false`.",
    "remediation": "Ensure that the search combobox updates its `aria-expanded` attribute properly. Example: `<input role=\"combobox\" aria-expanded=\"true\">` when expanded.",
    "wcag_reference": "4.1.2",
    "impact": "Screen reader users may be confused if `aria-expanded` does not correctly update on search elements.",
    "page_url": "file:///ruta/del/archivo/test_combobox.html",
    "resolution": "check_combobox_aria_expanded.md",
    "element_info": {
        "tag": "input",
        "text": "",
        "id": "searchBox",
        "class": "search-input",
        "line_number": 15
    }
}
✅ Beneficios del Tester
✔ Detecta errores de aria-expanded en comboboxes de búsqueda.
✔ Mejora la accesibilidad para usuarios de lectores de pantalla.
✔ Compatible con archivos HTML locales y páginas web dinámicas.
✔ Exporta los resultados a un archivo Excel automáticamente.

📢 ¡Corrige estos errores y mejora la experiencia de accesibilidad en tu sitio! 🚀