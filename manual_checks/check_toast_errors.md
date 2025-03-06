README - Check Toast Errors
Descripción
El tester check_toast_errors.py detecta si los mensajes de error tipo toast (notificaciones flotantes) desaparecen demasiado rápido antes de que el usuario pueda leerlos o interactuar con ellos.

Este problema es crítico en términos de accesibilidad, ya que los usuarios con baja visión, dificultades cognitivas o discapacidades motoras pueden necesitar más tiempo para leer y procesar la información.

Este problema está cubierto por la WCAG 2.2.1 - Tiempo Ajustable, que establece que los usuarios deben poder controlar el tiempo de visualización de los mensajes críticos.
🔗 WCAG 2.2.1 - Understanding Time Adjustable

🛠️ Cómo Funciona
El tester analiza el código HTML y:

Busca mensajes de error flotantes:
Elementos con clases comunes como .toast, .notification, .alert, .error-message
Verifica si desaparecen automáticamente en menos de min_duration segundos (valor por defecto: 5s).
Reporta un problema si desaparecen demasiado rápido, indicando:
Texto del mensaje de error.
Tiempo en el que desaparece automáticamente.
Impacto en usuarios con necesidades de accesibilidad.
Sugerencias para mejorar la accesibilidad.
🚨 Problema Detectado
Si un mensaje de error desaparece automáticamente antes de que el usuario pueda leerlo, el tester lo reportará con la siguiente información:

Título: "Error message disappears too quickly"
Severidad: Alta (High)
Impacto: Los usuarios pueden no darse cuenta del error y no comprender por qué no se envió el formulario.
Sugerencia de solución: Mantener el mensaje en pantalla hasta que el usuario lo cierre manualmente o mostrarlo cerca del campo del formulario.
📌 Ejemplo de Error en HTML
El siguiente código HTML representa un problema de accesibilidad donde un mensaje de error tipo toast desaparece automáticamente después de 2 segundos.

html
Copy
Edit
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Toast Error Test</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        .button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        .toast {
            display: none;
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            padding: 15px;
            background: red;
            color: white;
            border-radius: 5px;
        }
    </style>
</head>
<body>

    <h1>Prueba de Mensaje de Error con Timeout</h1>
    <button class="button" onclick="showToast()">Enviar formulario</button>

    <div id="errorToast" class="toast">❌ Error: El campo email es obligatorio.</div>

    <script>
        function showToast() {
            let toast = document.getElementById("errorToast");
            toast.style.display = "block";

            // ❌ Error: El mensaje desaparece automáticamente después de 2 segundos
            setTimeout(() => {
                toast.style.display = "none";
            }, 2000);
        }
    </script>

</body>
</html>
✅ Solución Recomendada
Para corregir el problema, el mensaje de error debe permanecer en pantalla hasta que el usuario lo cierre manualmente. En lugar de usar setTimeout, se puede agregar un botón de cierre explícito:

html
Copy
Edit
<button onclick="closeToast()">Cerrar</button>
javascript
Copy
Edit
function closeToast() {
    document.getElementById("errorToast").style.display = "none";
}
Otra alternativa es mostrar el mensaje de error dentro del formulario, cerca del campo correspondiente.

📌 Conclusión
Este tester ayuda a identificar errores de accesibilidad en mensajes tipo toast.
Los mensajes de error deben permanecer visibles hasta que el usuario los cierre.
No deben desaparecer automáticamente en menos de 5 segundos sin opción de ajuste.
Este tester ahora se puede integrar con global_tester.py para ejecutar la verificación en múltiples páginas automáticamente. 🚀