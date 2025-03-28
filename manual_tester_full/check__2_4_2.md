# 🧪 Tester WCAG 2.4.2 - Page Titled

Este tester verifica el cumplimiento del criterio **WCAG 2.4.2 - Page Titled (Nivel A)**, que exige que cada página web tenga un título que describa su tema o propósito.

---

## 📋 Descripción del Criterio

> **Criterio 2.4.2 - Page Titled**  
> Las páginas web deben tener títulos que describan su tema o propósito.

Esto permite a los usuarios:
- Identificar rápidamente el contenido de la página.
- Navegar entre pestañas o páginas abiertas con mayor facilidad.
- Ubicarse mejor al utilizar tecnologías de asistencia como lectores de pantalla.

---

## ✅ ¿Qué verifica el tester?

- Que exista un elemento `<title>` en el documento HTML.
- Que dicho `<title>` **no esté vacío**.
- Que el texto del `<title>` tenga al menos **3 palabras distintas** (como indicio de ser descriptivo).

---

## 🧪 Resultado del análisis

Si no se encuentra un `<title>` o está vacío/inadecuado, se genera una incidencia con la siguiente información:

| Campo                     | Valor                                                                 |
|--------------------------|-----------------------------------------------------------------------|
| **Título**               | Page lacks descriptive `<title>`                                     |
| **Bug Type**             | Page Title                                                           |
| **Prioridad**            | High                                                                 |
| **Expected Result**      | The page should contain a descriptive `<title>` in the `<head>`.     |
| **Actual Result**        | The `<title>` element is missing, empty, or too generic.             |
| **Recomendación**        | Use a meaningful title such as `<title>Formulario de Contacto</title>` |
| **Checkpoint WCAG**      | 2.4.2                                                                 |
| **Impacto en el usuario**| Users with assistive technology may not know what the page is about. |
| **Evidence**             | HTML tag context or `N/A`                                            |

---

## 💡 Ejemplo de HTML correcto

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>Formulario de Contacto - Clínica Sonrisa</title>
  </head>
  <body>
    ...
  </body>
</html>
📚 Referencias
Understanding WCAG 2.4.2 - Page Titled (W3C)

Técnica H25: Usar el elemento <title>

Técnica G88: Proveer títulos descriptivos