# 🧪 Tester WCAG 2.4.11 – Focus Not Obscured (Minimum)

Este tester verifica si existen elementos fijos (`position: fixed` o `sticky`) que podrían **ocultar completamente el foco del teclado**, violando así el criterio **WCAG 2.4.11 (Nivel AA)**.

---

## 📌 Criterio: 2.4.11 – Focus Not Obscured (Minimum)

**Objetivo:**  
Garantizar que cualquier componente de interfaz que reciba foco **permanezca al menos parcialmente visible** en la ventana del usuario.

> _“Cuando un componente de interfaz de usuario recibe foco mediante el teclado, no queda completamente oculto por contenido creado por el autor.”_

---

## ✅ ¿Qué detecta este tester?

Este script busca patrones que podrían ocultar el foco del teclado, como:

- Elementos con `position: fixed` o `sticky`
- Altura o ancho de `100%`
- `z-index` muy alto (`>= 9999`)
- `top: 0` o `bottom: 0` (pegados al borde de la pantalla)
- Headers fijos con altura ≥ 100px

Estos patrones suelen encontrarse en:

- Banners fijos
- Chat flotantes
- Notificaciones flotantes
- Headers pegajosos
- Overlays que cubren todo

---

## 📥 Input

- HTML de entrada (contenido de una página)
- URL de referencia para el reporte

---

## 📤 Output

- Archivo Excel (`issue_report.xlsx`) con incidencias detectadas
- Cada fila contiene:
  - Título del problema
  - Severidad
  - Paso a paso para reproducir
  - Evidencia extraída del HTML
  - Recomendación
  - Referencia WCAG 2.4.11

---

## 🧪 Ejemplo de HTML problemático

```html
<header style="position: fixed; top: 0; height: 120px; width: 100%; background: black;"></header>
<main style="margin-top: 200px;">
  <button>Focus me</button>
</main>
📁 Ubicación
Este tester debería ubicarse en la carpeta:

bash
Copy
Edit
manual_checks/testers_2_4_11_focus_not_obscured.py
🔧 Dependencias
beautifulsoup4

transform_json_to_excel.py (para exportar los resultados)

🧠 WCAG Referencia
WCAG 2.4.11 – Focus Not Obscured (Minimum)