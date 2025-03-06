📝 Verificación de Inclusión del Nombre del Sitio en el Título (check_page_title_site_name_auto_minimal.py)
📌 Descripción
Este tester analiza si el título de la página (<title>) incluye el nombre del sitio web. Se basa en la norma WCAG 2.4.2: Page Titled, que recomienda que los títulos sean descriptivos y ayuden a los usuarios a identificar en qué sitio web están.

🔍 Cómo Funciona
Busca el nombre del sitio en og:site_name

Si el HTML tiene <meta property="og:site_name" content="Sams Club">, usará ese valor.
Si no hay og:site_name, deriva el sitio desde el dominio

Si la URL es https://help.samsclub.com, detectará "Samsclub".
Verifica si el título de la página (<title>) contiene el nombre del sitio

Si <title>Centro de Ayuda</title> no incluye "Samsclub", genera una incidencia.
No reporta error si:

No se encuentra <title>.
No se puede deducir un nombre de sitio.
🚨 Problemas Detectados
🔴 Problema	🛠 Solución
El título de la página no contiene el nombre del sitio	Actualizar <title> para incluir el nombre del sitio.
✅ Ejemplo de HTML Correcto
Este código no generará incidencia, ya que el <title> incluye el nombre del sitio.

html
Copy
Edit
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centro de Ayuda - Sams Club</title>
    <meta property="og:site_name" content="Sams Club">
</head>
<body>
    <h1>Bienvenido al Centro de Ayuda</h1>
</body>
</html>
❌ Ejemplo de HTML con Problema
Este código sí generará incidencia, porque <title> no menciona el sitio.

html
Copy
Edit
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centro de Ayuda</title>
    <meta property="og:site_name" content="Sams Club">
</head>
<body>
    <h1>Bienvenido al Centro de Ayuda</h1>
</body>
</html>
Incidencia generada:

json
Copy
Edit
{
    "title": "Page title does not contain site name",
    "type": "Other A11y",
    "severity": "Medium",
    "description": "El título de la página 'Centro de Ayuda' no incluye el sitio 'Sams Club'.",
    "remediation": "Actualizar el <title> para que incluya el nombre del sitio web. Ejemplo: 'Centro de Ayuda - Sams Club'.",
    "wcag_reference": "2.4.2",
    "impact": "Los usuarios no sabrán fácilmente qué sitio están visitando."
}
🚀 Cómo Ejecutar el Tester
python
Copy
Edit
# Cargar contenido HTML de prueba
with open("test_page.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Ejecutar el tester
incidences = check_page_title_site_name_auto_minimal(html_content, "https://help.samsclub.com")
print(incidences)
📖 Referencia WCAG
2.4.2: Page Titled
El título debe describir el propósito de la página y ayudar a los usuarios a identificar el sitio.
Este tester ayuda a mejorar la navegabilidad y orientación del usuario al asegurarse de que los títulos de página sean claros y contengan el nombre del sitio web. 🔍✅