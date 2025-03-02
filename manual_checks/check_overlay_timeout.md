README - Check Overlay Timeout
Descripción
El tester check_overlay_timeout.py detecta si los overlays (ventanas emergentes, modales o popups) desaparecen demasiado rápido, antes de que el usuario pueda leer o interactuar con ellos. Esto es un problema de accesibilidad, ya que algunos usuarios pueden necesitar más tiempo para procesar la información o completar acciones dentro del overlay.

Este problema está cubierto por la WCAG 2.2.1 - Tiempo Ajustable, que establece que los usuarios deben tener control sobre los límites de tiempo o la posibilidad de extenderlos.
🔗 WCAG 2.2.1 - Understanding Time Adjustable

🛠️ Cómo Funciona
El tester realiza las siguientes acciones:

Busca botones o enlaces que abran overlays:
Elementos <button>, <a> con onclick, <div> con onclick
Elementos con la clase .button
Detecta overlays o modales en la página:
Elementos <div> o <dialog> con clases como overlay, popup, modal
Verifica si los overlays desaparecen automáticamente:
Si el overlay desaparece en menos de min_duration segundos (valor por defecto: 5s), se genera una incidencia.
🚨 Problema Detectado
Si un overlay desaparece antes de que el usuario tenga suficiente tiempo para leerlo o interactuar con él, el tester lo reportará con la siguiente información:

Título: "Overlay disappears too quickly"
Severidad: Alta (High)
Impacto: Usuarios con discapacidades visuales, motoras o cognitivas pueden no tener suficiente tiempo para interactuar con el contenido.
Sugerencia de solución: Mantener el overlay visible hasta que el usuario lo cierre manualmente o permitir que el tiempo sea configurable.
📌 Ejemplo de Error en HTML
El siguiente código HTML representa un problema de accesibilidad donde los overlays desaparecen automáticamente después de 3 segundos.

html
Copy
Edit
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Overlay Timeout Test</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        .button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        .overlay {
            display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 300px; padding: 20px; background: rgba(0, 0, 0, 0.8); color: white; border-radius: 8px;
            z-index: 1000;
        }
    </style>
</head>
<body>

    <h1>Prueba de Overlay con Timeout</h1>
    <button class="button" onclick="showOverlay('overlay1')">Abrir Overlay 1</button>
    <button class="button" onclick="showOverlay('overlay2')">Abrir Overlay 2</button>

    <div id="overlay1" class="overlay">Overlay 1 - Desaparece en 3s</div>
    <div id="overlay2" class="overlay">Overlay 2 - Desaparece en 3s</div>

    <script>
        function showOverlay(id) {
            let overlay = document.getElementById(id);
            overlay.style.display = "block";

            // ❌ Error: el overlay desaparece automáticamente después de 3 segundos
            setTimeout(() => {
                overlay.style.display = "none";
            }, 3000);
        }
    </script>

</body>
</html>
✅ Solución Recomendada
Para corregir el problema, el overlay debe permanecer en pantalla hasta que el usuario lo cierre manualmente. En lugar de usar setTimeout, se puede agregar un botón de cierre explícito:

html
Copy
Edit
<button onclick="closeOverlay('overlay1')">Cerrar</button>
javascript
Copy
Edit
function closeOverlay(id) {
    document.getElementById(id).style.display = "none";
}
📌 Conclusión
Este tester ayuda a identificar problemas de tiempo en overlays.
Los overlays deben permanecer en pantalla hasta que el usuario decida cerrarlos.
No deben desaparecer automáticamente en menos de 5 segundos sin opción de ajuste.
Este tester ahora se puede integrar con global_tester.py para ejecutar la verificación en múltiples páginas automáticamente. 🚀







