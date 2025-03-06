# Dropdown Contrast Tester

Este script analiza el contraste de las opciones seleccionadas (`selected`) y enfocadas (`hover`, `focus`, `checked`) dentro de elementos `<select>` en un documento HTML. Si el contraste es menor a 3:1, se genera un reporte con las incidencias encontradas.

## 🚀 Funcionalidades

✔️ Extrae estilos CSS desde etiquetas `<style>` internas en el HTML.  
✔️ Detecta reglas específicas para `option:selected`, `option:hover`, `option:focus`, `option:checked`.  
✔️ Soporta colores en formatos HEX (`#FFF`, `#FFFFFF`), `rgb()`, `rgba()`.  
✔️ Calcula la relación de contraste entre el color de texto y el fondo de cada opción.  
✔️ Reporta problemas de contraste si la relación es menor a **3:1**.  

---

## 📥 Instalación

Asegúrate de tener **Python 3.7+** instalado y las siguientes dependencias:

```sh
pip install beautifulsoup4
