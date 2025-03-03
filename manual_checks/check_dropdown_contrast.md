📌 README.md
md
Copy
Edit
# 🔍 Dropdown Selected Value Contrast Tester - `check_dropdown_contrast.py`

Este script detecta **problemas de contraste en las opciones seleccionadas de dropdowns (`<select>`)** cuando el usuario los expande.  
Si el texto seleccionado **no tiene suficiente contraste con el fondo**, puede dificultar la lectura para personas con baja visión.

## 📌 ¿Por qué es importante?
Según las **Directrices de Accesibilidad para el Contenido Web (WCAG 2.1)**:

- 📌 **El texto pequeño (<18px) debe tener un contraste mínimo de 4.5:1** respecto al fondo.
- 📌 **El texto grande (≥18px o 14px en negrita) debe tener un contraste mínimo de 3.0:1**.
- 📌 **Cuando un dropdown se expande, el texto seleccionado debe permanecer legible**.

Si el contraste es insuficiente, puede generar los siguientes problemas:

- ❌ **Usuarios con baja visión pueden no ver la opción seleccionada.**
- ❌ **No cumple con los estándares de accesibilidad de WCAG 2.1 (criterio 1.4.3).**
- ❌ **Dificulta la usabilidad del formulario y puede generar frustración en los usuarios.**

---

## ⚠️ **Problema Detectado**
El script analiza opciones seleccionadas en dropdowns (`<option selected>`) y **verifica la relación de contraste entre el color del texto y el fondo**.  
Ejemplo de código problemático:

### ❌ **Ejemplo Incorrecto (Con Error)**
```html
<select>
    <option value="dni">DNI</option>
    <!-- ❌ ERROR: Texto gris claro con fondo blanco, solo 1.73:1 de contraste -->
    <option value="nie" selected style="color: #BAC7CB; background-color: #FFFFFF;">NIE</option>
    <option value="passport">Pasaporte</option>
</select>
✅ Ejemplo Correcto (Solucionado)
html
Copy
Edit
<select>
    <option value="dni">DNI</option>
    <!-- ✅ CORRECTO: Texto azul oscuro con fondo blanco, mejora el contraste -->
    <option value="nie" selected style="color: #2C3E50; background-color: #FFFFFF;">NIE</option>
    <option value="passport">Pasaporte</option>
</select>
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
from check_dropdown_contrast import check_dropdown_contrast

with open("test_dropdown_contrast_error.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///ruta/del/archivo/test_dropdown_contrast_error.html"
incidencias = check_dropdown_contrast(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si el dropdown tiene bajo contraste en la opción seleccionada, el tester reportará:

json
Copy
Edit
{
    "title": "Dropdown selected value fails contrast once expanded",
    "type": "Color Contrast",
    "severity": "High",
    "description": "La opción seleccionada en el dropdown tiene un contraste de 1.73:1, lo que no cumple con el mínimo de 4.5:1 recomendado para texto pequeño.",
    "remediation": "Usar un color más oscuro para el texto o cambiar el fondo a un color con mayor contraste. Ejemplo: `color: #2C3E50;` en lugar de `color: #BAC7CB;`.",
    "wcag_reference": "1.4.3",
    "impact": "Los usuarios con baja visión no podrán leer el texto de la opción seleccionada.",
    "page_url": "file:///ruta/del/archivo/test_dropdown_contrast_error.html",
    "affected_element": "<option value='nie' selected style='color: #BAC7CB; background-color: #FFFFFF;'>NIE</option>"
}
✅ Beneficios del Tester
✔ Detecta opciones seleccionadas en dropdowns con contraste insuficiente.
✔ Verifica todos los dropdowns en la página, incluso si no tienen selected.
✔ Evalúa el contraste real de los colores, incluso si no están definidos en style.
✔ Genera reportes detallados con la relación de contraste y soluciones recomendadas.
✔ Fácil integración en global_tester.py.

💡 ¡Con este tester garantizamos que los dropdowns sean legibles para todos los usuarios! 🚀