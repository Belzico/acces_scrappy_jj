api_keyj=""

import openai
import os
from dotenv import load_dotenv

# Carga la clave desde variables de entorno (si lo deseas)
load_dotenv()
openai.api_key = api_keyj  # o pon "sk-..." directamente

def preguntar_a_chatgpt(pregunta):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Usa "gpt-4" si tu cuenta tiene acceso
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": pregunta}
        ]
    )
    return response.choices[0].message.content

# Ejemplo de uso
respuesta = preguntar_a_chatgpt("¿Cuál es la capital de Francia?")
print(respuesta)