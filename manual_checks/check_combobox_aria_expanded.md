📌 README.md
md
Copy
Edit
# 🔍 Combobox Accessibility Checker - `aria-expanded`

Este script verifica si los **comboboxes de búsqueda** tienen el atributo `aria-expanded` correctamente configurado.  
Si **el atributo `aria-expanded` no cambia entre "true" y "false" cuando el combobox se expande o colapsa**, se genera una incidencia.

## 📌 ¿Por qué es importante?
Los usuarios que navegan con lectores de pantalla como **JAWS (Chrome), NVDA (Firefox), TalkBack (Chrome) y VoiceOver (Safari)**  
**no pueden ver visualmente si el menú de búsqueda está abierto o cerrado**, por lo que necesitan que el estado expandido/colapsado se **anuncie correctamente**.

## ⚠️ Problema Detectado
- **Los comboboxes deben indicar su estado con `aria-expanded="true"` o `aria-expanded="false"`**.
- **Si `aria-expanded` no cambia cuando se expande o colapsa el combobox**, el usuario no sabrá si hay sugerencias visibles o no.
- **Esto causa confusión y una mala experiencia de usuario**.

### ❌ **Ejemplo Incorrecto**
```html
<input role="combobox" aria-expanded="false"> <!-- ❌ Nunca cambia a "true" al expandirse -->
<div role="combobox">Search here...</div> <!-- ❌ Sin aria-expanded -->
<select aria-expanded=""> <!-- ❌ Valor incorrecto -->
    <option>Option 1</option>
</select>
✅ Ejemplo Correcto
html
Copy
Edit
<input role="combobox" aria-expanded="false" 
       onfocus="this.setAttribute('aria-expanded', 'true')" 
       onblur="this.setAttribute('aria-expanded', 'false')"> <!-- ✅ Correcto -->

<div role="combobox" aria-expanded="false"
     onfocus="this.setAttribute('aria-expanded', 'true')"
     onblur="this.setAttribute('aria-expanded', 'false')">Search here...</div> <!-- ✅ Correcto -->

<select aria-expanded="false">
    <option>How to order online</option>
</select> <!-- ✅ Correcto -->
⚡ Instalación
Asegúrate de tener BeautifulSoup instalado:

bash
Copy
Edit
pip install beautifulsoup4
🚀 Uso del Tester
python
Copy
Edit
from check_combobox_aria_expanded import check_combobox_aria_expanded

with open("test_combobox_aria_expanded.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "https://example.com"
incidencias = check_combobox_aria_expanded(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si el combobox no cambia correctamente aria-expanded, el tester reportará:

json
Copy
Edit
{
    "title": "Aria-expanded attribute is not working correctly in Search combobox",
    "type": "Screen Reader",
    "severity": "Medium",
    "description": "Uno o más comboboxes de búsqueda no cambian correctamente el atributo `aria-expanded`. Cuando se expande el menú de búsqueda, `aria-expanded` debe cambiar a `true`, y cuando se colapsa, debe cambiar a `false`.",
    "remediation": "Actualizar el `aria-expanded` en el combobox de búsqueda para reflejar correctamente su estado. Ejemplo: `<input role=\"combobox\" aria-expanded=\"true\">` cuando está expandido.",
    "wcag_reference": "4.1.2",
    "impact": "Los usuarios con lectores de pantalla pueden sentirse confundidos si `aria-expanded` no cambia correctamente en la búsqueda.",
    "page_url": "https://example.com"
}
✅ Beneficios del Tester
Mejora la accesibilidad para usuarios con lectores de pantalla en escritorios y móviles.
Detecta automáticamente si falta aria-expanded en comboboxes de búsqueda.
Compatible con <input>, <div> y <select> con role="combobox".
Puede ejecutarse de forma independiente o integrarse en global_tester.py.
