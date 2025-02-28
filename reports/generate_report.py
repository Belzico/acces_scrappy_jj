import json
import pandas as pd

def generate_report(results, output_file="accessibility_report.csv"):
    """Genera un reporte CSV con problemas de accesibilidad encontrados"""
    data = []
    for result in results:
        for issue in result["violations"]:
            data.append({
                "url": result["url"],
                "impact": issue["impact"],
                "description": issue["description"],
                "help_url": issue["helpUrl"]
            })
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Reporte generado: {output_file}")

# Prueba con datos simulados
if __name__ == "__main__":
    with open("accessibility_results.json") as f:
        sample_results = json.load(f)
    
    generate_report(sample_results)
