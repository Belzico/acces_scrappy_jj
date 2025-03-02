📄 Verificación de Espaciado de Texto en Menús (check_menu_text_spacing.py)
🔍 Descripción
Este tester analiza los elementos de menú (<nav>, <ul>, <div class="menu">, etc.) en una página web para detectar si el texto se desborda o se corta cuando se aplican ajustes de espaciado de texto. Se basa en la normativa WCAG 1.4.12: Text Spacing, que exige que el contenido siga siendo legible y accesible cuando los usuarios aumentan el espaciado del texto.

🎯 Problemas Detectados
Contenido recortado (overflow: hidden;)

Si un elemento del menú tiene overflow: hidden, el contenido podría quedar oculto cuando los usuarios aumentan el espaciado de texto.
Texto que no se ajusta (white-space: nowrap;)

Si se detecta white-space: nowrap, el texto no podrá ajustarse correctamente y podría desbordarse fuera del contenedor.
Altura máxima fija (max-height: Xpx;)

Si el menú usa max-height con un valor en píxeles, podría impedir que los elementos internos se expandan correctamente, causando que parte del contenido quede oculto.
📌 Cómo Funciona
Busca menús y elementos de navegación (<nav>, <ul>, <div class="menu">, <div class="navbar">, etc.).
Revisa los estilos CSS embebidos (style="") en los elementos <li>, <a>, <span>, <div>.
Genera una incidencia si encuentra overflow: hidden, white-space: nowrap, o max-height en píxeles.
🚀 Ejemplo de HTML con Problema de Espaciado en Menús
Este código contiene errores que el tester debería detectar.

html
Copy
Edit
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prueba de Menú con Problemas de Espaciado</title>
    <style>
        .menu {
            background-color: #333;
            color: white;
            padding: 10px;
            overflow: hidden; /* ❌ Error: contenido podría cortarse */
            max-height: 50px; /* ❌ Error: elementos podrían no expandirse */
        }
        .menu-item {
            white-space: nowrap; /* ❌ Error: texto no se ajusta correctamente */
            display: block;
            padding: 5px 10px;
        }
    </style>
</head>
<body>

    <nav class="menu">
        <a href="#" class="menu-item">Inicio</a>
        <a href="#" class="menu-item">Nosotros</a>
        <a href="#" class="menu-item">Contacto</a>
    </nav>

    <p>Ajusta el espaciado del texto en tu navegador y observa si el contenido se corta o desborda.</p>

</body>
</html>
🔧 Cómo Ejecutar el Tester
python
Copy
Edit
# Cargar contenido HTML de prueba
with open("menu_test.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Ejecutar el tester
incidences = check_menu_text_spacing(html_content, "https://example.com")
print(incidences)
✅ Resultados Esperados
El tester debería detectar los siguientes errores en el HTML de prueba:

Contenido recortado (overflow: hidden;)
Texto que no se ajusta (white-space: nowrap;)
Menú con altura fija (max-height: 50px;)
Cada uno generará una incidencia con recomendaciones para corregirlos.

📖 Recomendaciones para Corregir los Errores
Evitar overflow: hidden; en menús
css
Copy
Edit
.menu {
    overflow: visible;
}
Permitir que el texto se ajuste automáticamente
css
Copy
Edit
.menu-item {
    white-space: normal;
}
Usar alturas dinámicas en menús
css
Copy
Edit
.menu {
    max-height: none;
    min-height: auto;
}
📚 Referencia WCAG
1.4.12: Text Spacing
Asegura que el contenido sea legible y accesible con espaciado de texto ajustado.
Este tester permite detectar problemas de accesibilidad en menús cuando los usuarios modifican el espaciado del texto en sus navegadores. 🔍 ✅