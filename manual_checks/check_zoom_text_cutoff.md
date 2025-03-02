Tester de Detección de Texto Cortado a 200% Zoom 🧐🔍
Este tester analiza el código HTML de una página web para identificar problemas de truncado de texto cuando el usuario amplía el contenido al 200% de zoom, según lo establecido en la norma WCAG 1.4.4 (Resize Text).

🔎 ¿Qué revisa este tester?
Elementos con overflow: hidden; → Puede ocultar contenido importante al hacer zoom.
Elementos con white-space: nowrap y text-overflow: ellipsis → Puede truncar texto y mostrar ... en lugar del contenido completo.
Clases problemáticas (truncate, text-cutoff, hidden, etc.) → Puede indicar que el texto está siendo visualmente recortado en la interfaz.
📝 Criterios de detección
Problema Detectado	Severidad	Descripción
Text may be cut off at 200% zoom	🔴 Alta	Se detectó overflow: hidden;, lo que puede ocultar texto importante.
Text truncation detected (inline style)	🔴 Alta	Se encontraron white-space: nowrap; y text-overflow: ellipsis;, lo que puede impedir que el usuario lea todo el texto.
Text truncation detected (class)	🔴 Alta	Se detectó una clase sospechosa como 'truncate', 'text-cutoff', 'hidden', que puede truncar el contenido en la interfaz.
📌 Recomendaciones de solución
Evitar overflow: hidden; en secciones con texto relevante.
Usar white-space: normal; y text-overflow: clip; para evitar el recorte del texto.
Permitir que el contenedor se expanda dinámicamente con min-height: auto; en lugar de alturas fijas.
Revisar clases problemáticas (truncate, text-cutoff) y garantizar que no oculten información clave.
📋 Ejemplo de HTML problemático
Este código causará problemas de truncado en el análisis:

html
Copy
Edit
<div class="truncate">
  Este texto será truncado porque usa estilos problemáticos.
</div>

<div style="white-space: nowrap; text-overflow: ellipsis; overflow: hidden; width: 250px;">
  Este texto se recortará con '...'.
</div>
🛠 Cómo probar este tester
Ejecutar el script sobre el contenido HTML de la página:
python
Copy
Edit
incidencias = check_zoom_text_cutoff(html_content, "https://ejemplo.com")
Verificar la salida JSON que reportará las incidencias encontradas.
📖 Referencias
WCAG 1.4.4: Resize Text
Guía de diseño accesible para zoom y reflow