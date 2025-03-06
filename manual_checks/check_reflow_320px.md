📝 README: Tester de Reflow en 320px (check_reflow_320px.py)
📌 Descripción
Este tester detecta problemas de reflujo cuando la página se visualiza a un ancho de 320px, asegurando que el contenido no requiera desplazamiento horizontal y se mantenga accesible según las pautas de WCAG 1.4.10: Reflow.

🔹 Objetivo: Identificar elementos con anchos fijos que causan desbordamiento en pantallas pequeñas.
🔹 Basado en: WCAG 1.4.10: Reflow
🔹 Revisión:

Elementos con width: Xpx fijos sin max-width.
Desplazamiento horizontal causado por overflow-x: scroll.
Estilos CSS embebidos (<style> en <head>).
Análisis de estilos inline (style="width: Xpx;").
🛠 Cómo Funciona
El tester analiza el contenido HTML en busca de reglas problemáticas que impidan que la página fluya correctamente en dispositivos móviles con un ancho de 320px.

1️⃣ Busca elementos con width: Xpx; sin max-width: 100%.
2️⃣ Detecta overflow-x: scroll, indicando la necesidad de desplazamiento horizontal.
3️⃣ Analiza los estilos embebidos en <style> dentro del <head>.
4️⃣ Genera incidencias si se encuentran problemas.

⚡ Ejemplo de Código Problemático
html
Copy
Edit
<div style="width: 600px;"> ❌ Esto causará un problema de reflujo </div>
css
Copy
Edit
.container {
    width: 800px; /* ❌ Este ancho fijo causará desplazamiento horizontal */
}
✅ Ejemplo de Código Corregido
html
Copy
Edit
<div style="max-width: 100%;"> ✅ Esto fluye correctamente </div>
css
Copy
Edit
.container {
    max-width: 100%; /* ✅ Solución para evitar el problema de reflujo */
}
🚀 Cómo Ejecutarlo
Este tester es llamado desde global_tester.py, por lo que se ejecuta automáticamente al analizar una página.

1️⃣ Asegúrate de incluir el tester en global_tester.py:

python
Copy
Edit
from manual_checks.check_reflow_320px import check_reflow_320px
TESTERS.append(check_reflow_320px)
2️⃣ Para probarlo manualmente, usa:

python
Copy
Edit
with open("test.html", "r", encoding="utf-8") as f:
    html_content = f.read()

incidences = check_reflow_320px(html_content, "test.html")
print(incidences)
📌 Impacto del Problema
🔹 Usuarios con discapacidad visual o motriz tendrán dificultades para navegar si el contenido requiere desplazamiento horizontal.
🔹 El contenido puede solaparse en pantallas pequeñas, dificultando la comprensión.
🔹 Es obligatorio para la conformidad con WCAG 2.1 (Criterio 1.4.10).

✅ Solución Recomendadas
✔ Evitar anchos fijos en píxeles, usar max-width: 100%.
✔ Revisar y corregir reglas CSS embebidas.
✔ Eliminar overflow-x: scroll innecesarios.
✔ Usar diseño responsivo (flexbox, grid y media queries).

📌 Referencias
🔗 WCAG 1.4.10: Reflow
🔗 Guía de CSS Responsive