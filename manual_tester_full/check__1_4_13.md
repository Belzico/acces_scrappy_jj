# WCAG 1.4.13 Accessibility Tester – Content on Hover or Focus

Este script analiza archivos HTML para detectar posibles violaciones del criterio **WCAG 2.1 – 1.4.13: Content on Hover or Focus** (Nivel AA), relacionado con contenido adicional que aparece al pasar el puntero (`hover`) o enfocar (`focus`) elementos interactivos.

---

## 🎯 ¿Qué verifica?

Detecta si el contenido adicional (como tooltips personalizados, popups o mensajes flotantes):

1. ✅ **Dismissible**: puede ser descartado (ej. con la tecla Escape)
2. ✅ **Hoverable**: permite mover el mouse sobre él sin desaparecer
3. ✅ **Persistent**: se mantiene visible hasta que el usuario lo cierre o pierda el foco voluntariamente

---

## 📂 Archivos

- `run_all___1_4_13.py`: script principal
- `transform_json_to_excel.py`: utilidad externa para exportar incidencias a Excel
- `README.md`: este archivo

---

## 🚀 Cómo usar

```bash
python run_all___1_4_13.py
O importar el método desde otro módulo:

python
Copy
Edit
from run_all___1_4_13 import run_all___1_4_13

with open("test.html", encoding="utf-8") as f:
    html = f.read()

resultados = run_all___1_4_13(html, page_url="https://ejemplo.com")
Esto generará un archivo issue_report.xlsx con las incidencias encontradas.

📋 Ejemplo de incidencia generada
Campo	Ejemplo
Title	Hover/Focus-triggered content may violate WCAG 1.4.13
Bug Type	Focus & Hover Interaction
Priority	Medium
Expected Result	Content must be dismissible, hoverable, and persistent.
Actual Result	Content does not provide a method for dismissal. Not persistent.
Suggested resolution(s)	Add Escape key handling, allow pointer over content, prevent auto-hide.
Failed checkpoint	1.4.13
Evidence	div[class=custom-tooltip, id=tip1, line=45]
🔎 ¿Qué elementos analiza?
El tester detecta contenido adicional usando:

role="tooltip"

Clases como tooltip, popup, popover, hint, hover

Atributos: data-tooltip, aria-describedby, aria-hidden

Referencias aria-describedby hacia elementos de contenido

🧠 Requisitos
Python 3.7+

beautifulsoup4

openpyxl (para exportar a Excel)

Instala dependencias:

bash
Copy
Edit
pip install beautifulsoup4 openpyxl
🧪 HTML de prueba
html
Copy
Edit
<button class="show-tooltip" aria-describedby="tip1">Hover me</button>
<div class="custom-tooltip" id="tip1" role="tooltip" style="display:none;">
  Ayuda flotante que se oculta automáticamente.
</div>
📘 Referencias
WCAG 2.1 – SC 1.4.13

Documentación oficial de WAI-ARIA