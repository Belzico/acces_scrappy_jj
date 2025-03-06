import pandas as pd
import os

# Campos originales del Excel con su mapeo al JSON
FIELD_MAPPING = {
    "To review": None,
    "Total": None,
    "Ident.": None,
    "Redac.": None,
    "Sol.": None,
    "SS": None,
    "CP": None,
    "Comments": "description",
    "Issue Title [Page section - Title]": "title",
    "Bug Type": "type",
    "Priority": "severity",
    "Action Performed [Steps]": "steps",
    "Expected Result": "expected_result",
    "Actual Result": "element_info",
    "Suggested resolution(s)": "remediation",
    "Evidence [SS or Video]": "resolution",
    "Page url":"page_url",
    "Failed checkpoint": "wcag_reference",
    "User Impact": "impact",
}

def transform_json_to_excel(json_data, excel_file):
    """
    Agrega datos de un JSON ya cargado a un archivo Excel existente, sin sobrescribirlo.
    Si hay campos en JSON que no existen en el Excel, se agregarán como nuevas columnas.

    :param json_data: Lista de objetos JSON ya cargada en memoria.
    :param excel_file: Ruta al archivo Excel donde se agregarán las filas.
    """

    # 1️⃣ Asegurar que el JSON es una lista de objetos
    if not isinstance(json_data, list):
        json_data = [json_data]

    # 2️⃣ Verificar si el archivo Excel ya existe
    if os.path.exists(excel_file):
        df_excel = pd.read_excel(excel_file)  # Cargar el archivo existente
    else:
        df_excel = pd.DataFrame(columns=FIELD_MAPPING.keys())  # Crear un DataFrame con columnas originales si no existe

    # 3️⃣ Crear una lista para almacenar las nuevas filas transformadas
    transformed_rows = []

    for item in json_data:
        row_data = {}

        # 4️⃣ Mapear los campos del JSON con los del Excel
        extra_fields = {}  # Para campos del JSON sin match en el Excel
        for excel_field, json_key in FIELD_MAPPING.items():
            if json_key and json_key in item:
                row_data[excel_field] = item[json_key]
            else:
                row_data[excel_field] = ""  # Campo vacío si no hay match

        # 5️⃣ Guardar los campos adicionales no mapeados
        for key, value in item.items():
            if key not in FIELD_MAPPING.values():  # Si el campo no tiene mapeo
                extra_fields[key] = value

        # Agregar los campos extra como columnas al final
        row_data.update(extra_fields)

        transformed_rows.append(row_data)

    # 6️⃣ Crear un DataFrame con los nuevos datos
    df_new_data = pd.DataFrame(transformed_rows)

    # 7️⃣ Verificar si hay nuevas columnas que no existen en el Excel
    for column in df_new_data.columns:
        if column not in df_excel.columns:
            df_excel[column] = ""  # Agregar columna vacía en el Excel original

    # 8️⃣ Concatenar los nuevos datos con el Excel existente
    df_final = pd.concat([df_excel, df_new_data], ignore_index=True)

    # 9️⃣ Guardar el resultado en el mismo archivo Excel
    df_final.to_excel(excel_file, index=False)

    print(f"✅ Datos agregados a: {excel_file}")

# 📌 Ejemplo de uso
# json_data = [{"title": "Missing heading", "severity": "High", "element_info": "Line 23"}]
# transform_json_to_excel(json_data, "accessibility_report.xlsx")
