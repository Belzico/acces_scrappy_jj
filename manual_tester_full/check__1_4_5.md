# WCAG 1.4.5 - Images of Text (OCR-based) Checker

Este módulo verifica el cumplimiento del criterio **1.4.5: Images of Text** de las [WCAG 2.2](https://www.w3.org/WAI/WCAG21/Understanding/images-of-text.html), asegurando que cualquier texto contenido dentro de imágenes esté disponible como texto real en la página.

## 📌 ¿Qué hace este tester?

✅ Aplica **OCR (Reconocimiento Óptico de Caracteres)** usando `pytesseract` para detectar si una imagen contiene texto.  
✅ Revisa si dicho texto está disponible en el atributo `alt` o en el contenido adyacente (hermanos inmediatos).  
✅ Si no hay alternativa textual equivalente, se genera una incidencia.

---

## 🧪 Dependencias

- [pytesseract](https://pypi.org/project/pytesseract/)
- [Pillow](https://pypi.org/project/Pillow/)
- `BeautifulSoup4`
- Un folder local `downloaded_images` con las imágenes a procesar.
- Tesseract OCR instalado en el sistema.

---

## ✅ Función principal

```python
run_all___1_4_5(html_content: str, page_url: str, images_folder="downloaded_images", excel="issue_report.xlsx") -> list
Parámetros:
html_content: HTML de la página.

page_url: URL o identificador de la página analizada.

images_folder: Carpeta local donde están descargadas las imágenes referenciadas en los <img>.

excel: Nombre del archivo de Excel de salida.

📊 Formato del reporte
Campo	Descripción
Title	Título del problema detectado
Steps	Pasos para reproducir
Bug Type	Tipo de error (Screen Reader)
Priority	Severidad (High)
Expected Result	Qué se espera que ocurra
Actual Result	Qué se encontró con el OCR
Suggested resolution(s)	Cómo solucionarlo
Failed checkpoint	Criterio WCAG 1.4.5
User Impact	Impacto para usuarios con discapacidades
Evidence [SS or Video]	Referencia técnica al <img> involucrado
🧠 Ejemplo de incidencia generada
json
Copy
Edit
{
  "Title": "Image of Text Possibly Used",
  "Bug Type": "Screen Reader",
  "Priority": "High",
  "Expected Result": "All textual content in images should be available as real HTML text, or at least replicated in the alt attribute or nearby content.",
  "Actual Result": "OCR detected text: 'Important Title Here...', but no equivalent text was found nearby.",
  "Suggested resolution(s)": "Use HTML text instead of an image when possible. If unavoidable, ensure the alt attribute or nearby text includes the same content.",
  "Failed checkpoint": "1.4.5",
  "User Impact": "Screen reader or zoom users may miss important visual text.",
  "Evidence [SS or Video]": "img[class=banner-title, id=img-title, line=101]"
}
📝 Consideraciones
El OCR puede fallar si la imagen está borrosa, distorsionada o mal formateada. Si ocurre un error de procesamiento, la imagen simplemente se ignora y no se reporta como incidencia.

Este checker es útil para detectar banners, títulos decorativos o textos embebidos en imágenes que no tienen alternativa accesible.

Este módulo forma parte del sistema de auditoría de accesibilidad automatizada basado en WCAG 2.2.