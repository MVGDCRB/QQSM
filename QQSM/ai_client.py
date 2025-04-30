import asyncio
from requests import Session
from openai import OpenAI
import google.generativeai as gia
from QQSM.secrets import Secrets


class AIClient:

    # Configuración al importar el módulo
    gia.configure(api_key=Secrets.GIA_API_KEY)
    _model = gia.GenerativeModel("gemini-2.0-flash")
    
    def askAI(prompt: str): #askGemini?
        return AIClient._model.generate_content(prompt).text



    def askDeepSeek(prompt: str):
        api_key = Secrets.DEEP_API_KEY
        api_url = "https://api.deepseek.com/v1/chat/completions"  # Reemplaza con la URL correcta
        sesion = Session()

        # Configura los headers con tu clave de API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Define el cuerpo de la solicitud
        data = {
            "model": "deepseek-chat",  # Reemplaza con el modelo correcto
            "messages": [
                {
                    "role": "user",  # El rol del mensaje (en este caso, el usuario)
                    "content": prompt  # El contenido del mensaje
                }
            ],
            "max_tokens": 70,  # Ajusta según la longitud esperada de la respuesta, influye en el tiempo
            "temperature": 1,  # Controla la creatividad de la respuesta
            "stream": False
        }

        # Hacer la solicitud POST a la API
        response = sesion.post(api_url, headers=headers, json=data, timeout=15)

        # Verificar la respuesta
        if response.status_code == 200:
            # Extraer y mostrar la respuesta
            result = response.json()
            result = result["choices"][0]["message"]["content"]
            print(result)

            sesion.close()
            return result
        else:
            return "Error en la solicitud a la API."


    def askOpenAI(prompt: str):
        client = OpenAI(api_key=Secrets.OPEN_API_KEY)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user","content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )

        print(completion)
        return completion.choices[0].message.content

    
    def askLlamaAI(prompt: str):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=Secrets.LLAMA_API_KEY,
            base_url="https://api.llmapi.com/"
        )

        result = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
            ],
            model="llama4-maverick",
            stream=False
        )

        return result.choices[0].message.content
    

    def callGemini(prompt: str):
        api_key = "sk-0c4a68c97ce14b288ec1a6b5b9117e21"
        api_url = "https://api.deepseek.com/v1/chat/completions"  # Reemplaza con la URL correcta
        sesion = Session()

        # Configura los headers con tu clave de API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Define el cuerpo de la solicitud
        data = {
            "model": "deepseek-chat",  # Reemplaza con el modelo correcto
            "messages": [
                {
                    "role": "user",  # El rol del mensaje (en este caso, el usuario)
                    "content": prompt  # El contenido del mensaje
                }
            ],
            "max_tokens": 70,  # Ajusta según la longitud esperada de la respuesta, influye en el tiempo
            "temperature": 1,  # Controla la creatividad de la respuesta
            "stream": False
        }

        # Hacer la solicitud POST a la API
        response = sesion.post(api_url, headers=headers, json=data, timeout=15)

        # Verificar la respuesta
        if response.status_code == 200:
            # Extraer y mostrar la respuesta
            result = response.json()
            result = result["choices"][0]["message"]["content"]
            result = result.split(";")
            sesion.close()
            return result
        return None