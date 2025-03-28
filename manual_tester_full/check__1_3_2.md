# 🧪 Tester WCAG 1.3.2 – Meaningful Sequence

Este tester analiza si el contenido de una página HTML conserva una **secuencia significativa** que pueda ser **programáticamente determinada**, en cumplimiento con el criterio [WCAG 2.2 - 1.3.2: Meaningful Sequence (Nivel A)](https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html).

---

## ✅ ¿Qué verifica?

Este tester detecta automáticamente:

- 🔁 **Tablas de maquetación** (layout tables) que no incluyen `<th>`, `<caption>` ni `role="presentation"`, y que podrían desordenar la lectura secuencial del contenido (→ F49).
- 🎯 **Elementos con `position: absolute;`** que alteran la ubicación visual respecto al DOM, lo que podría romper el orden de lectura (→ F1).

---

## 📄 ¿Por qué es importante?

El orden en que se presenta el contenido es esencial para usuarios que dependen de tecnologías de asistencia como lectores de pantalla. Este tester busca identificar casos en los que:

- El contenido **puede ser leído fuera de orden**.
- La **presentación visual y el orden en el DOM no coinciden** y afectan el significado.
- No hay una secuencia lógica detectable para el usuario.

---

## 📤 Salida del reporte

Cada incidencia se formatea con:

| Campo                    | Descripción |
|-------------------------|-------------|
| Title                   | Título de la incidencia detectada. |
| Steps                   | Pasos para replicar y revisar la incidencia. |
| Bug Type                | Tipo de error (Meaningful Sequence). |
| Priority                | Nivel de severidad. |
| Expected Result         | Resultado esperado según WCAG. |
| Actual Result           | Resultado encontrado en el análisis. |
| Suggested resolution(s) | Sugerencia de solución accesible. |
| Failed checkpoint       | Criterio WCAG fallido (`1.3.2`). |
| User Impact             | Impacto para el usuario final. |
| Evidence                | Evidencia estructural del elemento afectado (selector rastreable). |

Los resultados se exportan a un archivo Excel si se encuentran incidencias.

---

## 🧪 Ejemplo de ejecución

```python
from testers_1_3_2 import run_all___1_3_2

with open("test_1_3_2.html", "r", encoding="utf-8") as f:
    html_content = f.read()

issues = run_all___1_3_2(html_content, page_url="test_1_3_2.html", excel="issues_1_3_2.xlsx")
📦 Archivos relacionados
Archivo	Descripción
testers_1_3_2.py	Código principal del tester.
test_1_3_2.html	HTML de prueba con errores típicos de secuencia.
issues_1_3_2.xlsx	Reporte generado tras el análisis.
📚 Referencias
WCAG 2.2 – 1.3.2: Meaningful Sequence

F49 – HTML layout table without proper linearization

F1 – CSS positioning that alters reading order

🤝 Contribuye
¿Te gustaría extender este tester para incluir detección de orden visual vs DOM? ¡Envíanos tus sugerencias o pull requests!