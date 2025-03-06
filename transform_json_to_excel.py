import json
import pandas as pd

# Mapeo de los campos del JSON con los del Excel
FIELD_MAPPING = {
    "To review": None,
    "Total": None,
    "Ident.": None,
    "Redac.": None,
    "Sol.": None,
    "SS": None,
    "CP": None,
    "Comments": "comments",
    "Issue Title [Page section - Title]": "title",
    "Bug Type": "bug_type",
    "Priority": "priority",
    "Action Performed [Steps]": "steps",
    "Expected Result": "expected_result",
    "Actual Result": "actual_result",
    "Suggested resolution(s)": "suggested_resolutions",
    "Evidence [SS or Video]": "evidence",
    "Failed checkpoint": "failed_checkpoint",
    "User Impact": "user_impact",
}

def transform_json_to_excel(json_file, excel_file, output_excel):
    """
    Transforma un archivo JSON en un Excel con los campos mapeados.

    :param json_file: Ruta al archivo JSON de entrada.
    :param excel_file: Ruta al archivo Excel de entrada.
    :param output_excel: Ruta donde se guardará el nuevo archivo Excel.
    """

    # 1️⃣ Leer el JSON
    with open(json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # Asegurar que el JSON es una lista de objetos
    if not isinstance(json_data, list):
        json_data = [json_data]

    # 2️⃣ Leer el Excel de entrada
    df_excel = pd.read_excel(excel_file)

    # 3️⃣ Crear una lista para almacenar las filas transformadas
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

    # 6️⃣ Crear un DataFrame con los datos transformados
    df_transformed = pd.DataFrame(transformed_rows)

    # 7️⃣ Guardar el resultado en un nuevo Excel
    df_transformed.to_excel(output_excel, index=False)

    print(f"✅ Transformación completada. Archivo guardado en: {output_excel}")

# 📌 Ejemplo de uso
# transform_json_to_excel("input.json", "template.xlsx", "output.xlsx")
