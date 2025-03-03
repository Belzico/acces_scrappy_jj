📌 README.md
md
Copy
Edit
# 🔍 Duplicated ID Detector - `check_duplicate_ids.py`

Este script verifica si hay **identificadores (`id`) duplicados** en el código HTML.  
Si **un mismo `id` aparece más de una vez**, puede causar problemas en **accesibilidad, compatibilidad con scripts y tecnologías asistivas**.

## 📌 ¿Por qué es importante?
Los **identificadores (`id`) deben ser únicos en el DOM**.  
Cuando un `id` está duplicado, puede generar los siguientes problemas:

- ❌ **Lectores de pantalla y tecnologías asistivas no podrán interpretar correctamente la página**.
- ❌ **Los scripts de JavaScript pueden seleccionar el elemento incorrecto**, causando fallos en la funcionalidad.
- ❌ **El HTML no será válido**, lo que puede generar incompatibilidades entre navegadores.

---

## ⚠️ **Problema Detectado**
El script busca elementos con `id` duplicados en el DOM.  
Ejemplo de código problemático:

### ❌ **Ejemplo Incorrecto (Con Duplicados)**
```html
<button id="passwordPositions">Continuar</button>
<button id="passwordPositions">Reenviar Código</button>
<div id="passwordPositions">Este es un mensaje oculto</div>
✅ Ejemplo Correcto (IDs Únicos)
html
Copy
Edit
<button id="passwordPositions_1">Continuar</button>
<button id="passwordPositions_2">Reenviar Código</button>
<div id="messageContainer">Este es un mensaje oculto</div>
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
from check_duplicate_ids import check_duplicate_ids

with open("test_duplicate_ids_error.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///ruta/del/archivo/test_duplicate_ids_error.html"
incidencias = check_duplicate_ids(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si hay id duplicados en la página, el tester reportará:

json
Copy
Edit
{
    "title": "Duplicated id in fields",
    "type": "HTML Validator",
    "severity": "High",
    "description": "Uno o más elementos en la página tienen el mismo `id`, lo que puede causar problemas en tecnologías asistivas y scripts de la web. Cada `id` debe ser único en el DOM.",
    "remediation": "Asegurar que cada `id` en la página sea único. Si necesitas múltiples instancias, usa `class` o añade un sufijo único, como `id=\"passwordPositions_1\"`.",
    "wcag_reference": "4.1.1",
    "impact": "Los usuarios que dependen de tecnologías asistivas pueden no recibir el contenido correctamente.",
    "page_url": "file:///ruta/del/archivo/test_duplicate_ids_error.html",
    "duplicated_ids": {
        "passwordPositions": ["button", "button", "div"],
        "documentNumber": ["input", "span"]
    }
}
✅ Beneficios del Tester
✔ Detecta TODOS los elementos con id, sin importar su tipo (button, div, span, input, etc.).
✔ Muestra en qué etiquetas (tag) se repite cada id.
✔ Genera un reporte detallado para corregir los problemas fácilmente.
✔ Compatible con cualquier estructura de HTML y scripts dinámicos.
✔ Fácil integración en global_tester.py.

💡 ¡Ahora garantizamos que TODOS los id sean únicos en la página! 🚀