📌 README.md
md
Copy
Edit
# 🔍 Placeholder Contrast Tester - `check_placeholder_contrast.py`

Este script detecta **problemas de contraste en el texto de los placeholders (`placeholder="Texto"`)** cuando se muestran en un fondo blanco.  
Si el placeholder **no tiene suficiente contraste con el fondo**, puede ser difícil de leer para personas con baja visión.

## 📌 ¿Por qué es importante?
Según las **Directrices de Accesibilidad para el Contenido Web (WCAG 2.1)**:

- 📌 **El texto pequeño (<18px) debe tener un contraste mínimo de 4.5:1** respecto al fondo.
- 📌 **El texto grande (≥18px o 14px en negrita) debe tener un contraste mínimo de 3.0:1**.
- 📌 **Si el contraste es insuficiente, el placeholder será ilegible para algunos usuarios**.

Si el contraste es bajo, puede generar los siguientes problemas:

- ❌ **Los usuarios con baja visión pueden no ver el texto del placeholder.**
- ❌ **No cumple con los estándares de accesibilidad de WCAG 2.1 (criterio 1.4.3).**
- ❌ **Los formularios pueden volverse difíciles de completar.**

---

## ⚠️ **Problema Detectado**
El script analiza inputs con placeholder y **verifica la relación de contraste entre el color del texto y el fondo**.  
Ejemplo de código problemático:

### ❌ **Ejemplo Incorrecto (Con Error)**
```html
<input type="text" placeholder="Introduce tu número de documento" style="color: #BFCAD1; background-color: #FFFFFF;">
🛑 Problema: Color del placeholder #BFCAD1 sobre fondo #FFFFFF, relación de contraste = 1.66:1 (No accesible).

✅ Ejemplo Correcto (Solucionado)
html
Copy
Edit
<input type="text" placeholder="Introduce tu número de documento" style="color: #757575; background-color: #FFFFFF;">
✅ Solución: Color del placeholder #757575 sobre fondo #FFFFFF, relación de contraste = 4.6:1 (Accesible).

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
from check_placeholder_contrast import check_placeholder_contrast

with open("test_placeholder_contrast_error.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///ruta/del/archivo/test_placeholder_contrast_error.html"
incidencias = check_placeholder_contrast(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si el placeholder tiene bajo contraste con el fondo, el tester reportará:

json
Copy
Edit
{
    "title": "Grey placeholder fails contrast on white background",
    "type": "Color Contrast",
    "severity": "High",
    "description": "El placeholder en el campo de entrada tiene un contraste de 1.66:1, lo que no cumple con el mínimo de 4.5:1 recomendado para texto pequeño.",
    "remediation": "Usar un color más oscuro para el texto del placeholder o cambiar el fondo a un color con mayor contraste. Ejemplo: `color: #757575;` en lugar de `color: #BFCAD1;`.",
    "wcag_reference": "1.4.3",
    "impact": "Los usuarios con baja visión no podrán leer el texto del placeholder.",
    "page_url": "file:///ruta/del/archivo/test_placeholder_contrast_error.html",
    "affected_element": "<input type='text' placeholder='Introduce tu número de documento' style='color: #BFCAD1; background-color: #FFFFFF;'>"
}
✅ Beneficios del Tester
✔ Detecta placeholders con bajo contraste en campos de entrada.
✔ Evalúa todos los inputs con placeholders en la página.
✔ Genera reportes detallados con la relación de contraste y soluciones recomendadas.
✔ Fácil integración en global_tester.py.

💡 ¡Con este tester garantizamos que los placeholders sean legibles para todos los usuarios! 🚀