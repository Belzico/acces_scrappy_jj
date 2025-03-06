import subprocess
import json
import os

LIGHTHOUSE_EXECUTABLE = "C:\\Users\\namic\\AppData\\Roaming\\npm\\lighthouse.cmd"
LIGHTHOUSE_OPTIONS = [
    "--only-categories=accessibility",
    "--quiet",
    "--no-enable-error-reporting",
    "--output=json"
]

def analyze_lighthouse(url):
    """
    Ejecuta Google Lighthouse para evaluar accesibilidad en la URL dada y filtra solo los errores detectados.

    :param url: (str) La URL de la página a analizar.
    :return: (list) Lista de errores de accesibilidad detectados.
    """

    output_path = "lighthouse_report.json"

    command = [
        LIGHTHOUSE_EXECUTABLE, url,
        *LIGHTHOUSE_OPTIONS,
        f"--output-path={output_path}"
    ]

    try:
        print(f"🚀 Ejecutando Lighthouse en {url}...")
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if not os.path.exists(output_path):
            raise FileNotFoundError("Lighthouse no generó el archivo esperado.")

        with open(output_path, "r", encoding="utf-8") as file:
            report = json.load(file)

        # 📌 Extraer solo la categoría de accesibilidad
        accessibility_audits = report["categories"]["accessibility"]["auditRefs"]
        audits = report["audits"]

        errors = []
        for audit in accessibility_audits:
            audit_id = audit["id"]
            audit_data = audits.get(audit_id, {})

            # Obtener el puntaje (score) de la auditoría, asegurando que no sea None
            score = audit_data.get("score", 1.0)
            if score is None or (isinstance(score, (int, float)) and score < 1.0):
                errors.append({
                    "id": audit_id,
                    "title": audit_data.get("title"),
                    "description": audit_data.get("description"),
                    "help_url": audit_data.get("help"),
                    "nodes": audit_data.get("details", {}).get("items", [])
                })

        return errors

    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar Lighthouse: {e}")
        return [{"url": url, "error": str(e)}]

    except Exception as e:
        print(f"⚠️ Lighthouse falló: {e}")
        return [{"url": url, "error": str(e)}]
