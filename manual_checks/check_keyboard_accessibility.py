from bs4 import BeautifulSoup
import re

def get_element_info(element):
    """Obtiene información útil de un elemento HTML para facilitar la localización del error."""
    return {
        "tag": element.name,
        "text": element.get_text(strip=True)[:50],  # Primeros 50 caracteres del texto
        "id": element.get("id", "N/A"),
        "class": " ".join(element.get("class", [])) if element.has_attr("class") else "N/A",
        "line_number": element.sourceline if hasattr(element, 'sourceline') else "N/A"  # Obtiene el número de línea si es posible
    }

def check_keyboard_accessibility(html_content, page_url):
    """
    Tester para WCAG 2.1.1 - Keyboard Accessibility.
    Detecta eventos de mouse sin equivalentes de teclado en HTML y JavaScript.
    """

    incidences = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 1️⃣ Elementos con eventos de mouse pero sin equivalentes de teclado
    elements_with_mouse_events = soup.find_all(onclick=True) + soup.find_all(onmouseover=True) + soup.find_all(onmouseenter=True)

    for element in elements_with_mouse_events:
        element_info = get_element_info(element)
        missing_keyboard_support = []

        # Verificar si no tiene eventos equivalentes de teclado
        if "onkeydown" not in element.attrs and "onkeypress" not in element.attrs:
            missing_keyboard_support.append("onkeydown")

        if "onfocus" not in element.attrs and ("onmouseover" in element.attrs or "onmouseenter" in element.attrs):
            missing_keyboard_support.append("onfocus")

        # Verificar si es un span o div con onclick y sin tabindex
        if element.name in ["span", "div"] and "onclick" in element.attrs and "tabindex" not in element.attrs:
            missing_keyboard_support.append("tabindex='0'")

        if missing_keyboard_support:
            incidences.append({
                "title": "Elemento con evento de mouse sin soporte de teclado",
                "type": "Keyboard Accessibility",
                "severity": "High",
                "description": f"El elemento tiene {', '.join(element.attrs.keys())} pero le falta {', '.join(missing_keyboard_support)}.",
                "remediation": f"Asegurar que {', '.join(missing_keyboard_support)} estén presentes para accesibilidad con teclado.",
                "wcag_reference": "2.1.1",
                "impact": "Usuarios sin mouse no pueden interactuar con este elemento.",
                "page_url": page_url,
                "element_info": element_info
            })

    # 2️⃣ Revisar etiquetas <script> en busca de problemas de accesibilidad en JavaScript
    script_tags = soup.find_all("script")

    js_patterns = {
        "click_no_keydown": re.compile(r'\.addEventListener\s*\(\s*["\']click["\']'),
        "mouseover_no_focus": re.compile(r'\.addEventListener\s*\(\s*["\']mouseover["\']'),
        "mouseenter_no_focus": re.compile(r'\.addEventListener\s*\(\s*["\']mouseenter["\']'),
        "hidden_no_aria": re.compile(r'\.style\.display\s*=\s*["\']none["\']')
    }

    for script in script_tags:
        script_content = script.string
        if not script_content:
            continue

        script_info = get_element_info(script)

        # Detectar `click` sin `keydown`
        if js_patterns["click_no_keydown"].search(script_content) and "keydown" not in script_content:
            incidences.append({
                "title": "Manejador de 'click' sin 'keydown'",
                "type": "Keyboard Accessibility",
                "severity": "High",
                "description": "Se encontró `addEventListener('click', ...)` sin un equivalente `keydown`.",
                "remediation": "Agregar `addEventListener('keydown', ...)` para accesibilidad con teclado.",
                "wcag_reference": "2.1.1",
                "impact": "Usuarios que navegan con teclado no podrán activar la función.",
                "page_url": page_url,
                "element_info": script_info
            })

        # Detectar `mouseover` sin `focus`
        if js_patterns["mouseover_no_focus"].search(script_content) and "focus" not in script_content:
            incidences.append({
                "title": "Manejador de 'mouseover' sin 'focus'",
                "type": "Keyboard Accessibility",
                "severity": "Medium",
                "description": "Se encontró `addEventListener('mouseover', ...)` sin un equivalente `focus`.",
                "remediation": "Agregar `addEventListener('focus', ...)` para accesibilidad con teclado.",
                "wcag_reference": "2.1.1",
                "impact": "Usuarios sin mouse no pueden interactuar con el contenido.",
                "page_url": page_url,
                "element_info": script_info
            })

        # Detectar `mouseenter` sin `focus`
        if js_patterns["mouseenter_no_focus"].search(script_content) and "focus" not in script_content:
            incidences.append({
                "title": "Manejador de 'mouseenter' sin 'focus'",
                "type": "Keyboard Accessibility",
                "severity": "Medium",
                "description": "Se encontró `addEventListener('mouseenter', ...)` sin un equivalente `focus`.",
                "remediation": "Agregar `addEventListener('focus', ...)` para accesibilidad con teclado.",
                "wcag_reference": "2.1.1",
                "impact": "Usuarios sin mouse no pueden interactuar con el contenido.",
                "page_url": page_url,
                "element_info": script_info
            })

        # Detectar elementos ocultos sin `aria-hidden`
        if js_patterns["hidden_no_aria"].search(script_content) and "aria-hidden" not in script_content:
            incidences.append({
                "title": "Elemento oculto sin 'aria-hidden'",
                "type": "Keyboard Accessibility",
                "severity": "Low",
                "description": "Se encontró `element.style.display = 'none'` sin `aria-hidden`.",
                "remediation": "Agregar `element.setAttribute('aria-hidden', 'true')` cuando el contenido se oculta.",
                "wcag_reference": "2.1.1",
                "impact": "Usuarios de lectores de pantalla podrían no ser informados sobre cambios de visibilidad.",
                "page_url": page_url,
                "element_info": script_info
            })

    # 3️⃣ **Nuevo: Detectar `data-event="mouseover"` sin equivalente de teclado**
    elements_with_data_event = soup.find_all(attrs={"data-event": "mouseover"})
    
    for element in elements_with_data_event:
        element_info = get_element_info(element)
        if "onfocus" not in element.attrs:
            incidences.append({
                "title": "Elemento con 'data-event=\"mouseover\"' sin 'onfocus'",
                "type": "Keyboard Accessibility",
                "severity": "Medium",
                "description": "El elemento usa 'data-event=\"mouseover\"' pero no tiene 'onfocus'.",
                "remediation": "Agregar 'onfocus' para permitir la activación mediante teclado.",
                "wcag_reference": "2.1.1",
                "impact": "Usuarios sin mouse no podrán activar el evento con el teclado.",
                "page_url": page_url,
                "element_info": element_info
            })

    return incidences
