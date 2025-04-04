import pandas as pd

def contar_palabras_excel(ruta_archivo):
    df = pd.read_excel(ruta_archivo, sheet_name=None)  # Carga todas las hojas
    total_palabras = 0

    for hoja, datos in df.items():
        for col in datos.columns:
            for celda in datos[col]:
                if isinstance(celda, str):
                    total_palabras += len(celda.split())

    return total_palabras

# Ejemplo de uso
archivo = "issue_report.xlsx"
print(f"Palabras totales en el Excel: {contar_palabras_excel(archivo)}")
