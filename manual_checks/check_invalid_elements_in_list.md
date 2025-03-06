📌 README.md
md
Copy
Edit
# 🔍 Invalid Elements in List Detector - `check_invalid_elements_in_list.py`

Este script verifica si **listas desordenadas (`<ul>`) y listas ordenadas (`<ol>`) contienen elementos `<div>` de manera incorrecta**.  
Si **un `<ul>` o `<ol>` tiene `<div>` en lugar de `<li>` como hijos directos**, puede generar problemas en validación HTML, compatibilidad y accesibilidad.

## 📌 ¿Por qué es importante?
Los **elementos `<ul>` y `<ol>` solo deben contener `<li>`, `<script>` o `<template>` como hijos directos**.  
Cuando un `<div>` está directamente dentro de `<ul>` o `<ol>`, puede causar:

- ❌ **Errores en validadores HTML**.
- ❌ **Problemas con estilos CSS y JavaScript**.
- ❌ **Dificultades para tecnologías asistivas y screen readers**.

---

## ⚠️ **Problema Detectado**
El script busca `<div>` dentro de `<ul>` o `<ol>` sin estar envueltos en `<li>`.  
Ejemplo de código problemático:

### ❌ **Ejemplo Incorrecto (Con Error)**
```html
<ul>
    <div class="menu-item">Inicio</div>
    <div class="menu-item">Productos</div>
</ul>
✅ Ejemplo Correcto (Solucionado)
html
Copy
Edit
<ul>
    <li><div class="menu-item">Inicio</div></li>
    <li><div class="menu-item">Productos</div></li>
</ul>
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
from check_invalid_elements_in_list import check_invalid_elements_in_list

with open("test_ul_ol_with_div_error.html", "r", encoding="utf-8") as f:
    html_content = f.read()

page_url = "file:///ruta/del/archivo/test_ul_ol_with_div_error.html"
incidencias = check_invalid_elements_in_list(html_content, page_url)

for inc in incidencias:
    print(inc)
📄 Ejemplo de Incidencia Detectada
Si hay <div> dentro de <ul> o <ol>, el tester reportará:

json
Copy
Edit
{
    "title": "Div elements nested into the ul/ol in the navigation menu",
    "type": "HTML Validator",
    "severity": "Low",
    "description": "El elemento `<ul>` o `<ol>` no debe contener `<div>` directamente como hijo. Solo `<li>`, `<script>` o `<template>` están permitidos dentro de listas.",
    "remediation": "Asegurar que los `<div>` dentro de `<ul>` o `<ol>` estén dentro de `<li>`. Ejemplo: `<li><div class=\"menu-item\">Inicio</div></li>`.",
    "wcag_reference": "4.1.1",
    "impact": "No hay impacto inmediato, pero puede causar problemas de validación y compatibilidad futura.",
    "page_url": "file:///ruta/del/archivo/test_ul_ol_with_div_error.html",
    "affected_elements": [
        "<ul>...</ul>",
        "<ol>...</ol>"
    ]
}
✅ Beneficios del Tester
✔ Detecta si un <ul> o <ol> contiene <div> directamente sin <li>.
✔ Genera un reporte con los <ul> y <ol> afectados.
✔ Mejora la compatibilidad y validación HTML en navegadores.
✔ Fácil integración en global_tester.py.

💡 ¡Con este tester garantizamos que las listas sean estructuradas correctamente en HTML! 🚀