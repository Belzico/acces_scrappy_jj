from bs4 import BeautifulSoup

def check_invalid_elements_in_list(html_content, page_url):
    """
    Verifica si existen `<div>` anidados directamente dentro de `<ul>` o `<ol>`.

    - Busca todas las listas `<ul>` y `<ol>`.
    - Verifica si contienen `<div>` directamente en su interior.
    - Si encuentra problemas, genera una incidencia.
    """

    # 1) Parsear el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 2) Buscar todas las listas <ul> y <ol>
    list_elements = soup.find_all(["ul", "ol"])

    # 3) Buscar <div> dentro de <ul> o <ol> sin un <li> como contenedor
    invalid_lists = []
    for lst in list_elements:
        for child in lst.find_all(recursive=False):  # Solo hijos directos
            if child.name == "div":
                invalid_lists.append(lst)

    # 4) Generar incidencias si hay <div> dentro de <ul> o <ol>
    incidencias = []
    if invalid_lists:
        incidencias.append({
            "title": "Div elements nested into the ul/ol in the navigation menu",
            "type": "HTML Validator",
            "severity": "Low",
            "description": (
                "El elemento `<ul>` o `<ol>` no debe contener `<div>` directamente como hijo. "
                "Solo `<li>`, `<script>` o `<template>` están permitidos dentro de listas."
            ),
            "remediation": (
                "Asegurar que los `<div>` dentro de `<ul>` o `<ol>` estén dentro de `<li>`. "
                "Ejemplo: `<li><div class=\"menu-item\">Inicio</div></li>`."
            ),
            "wcag_reference": "4.1.1",
            "impact": "No hay impacto inmediato, pero puede causar problemas de validación y compatibilidad futura.",
            "page_url": page_url,
            "affected_elements": [str(lst) for lst in invalid_lists]  # Lista de listas con errores
        })

    return incidencias
