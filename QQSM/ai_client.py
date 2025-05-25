import asyncio
from requests import Session
from openai import OpenAI
import google.generativeai as gia
from QQSM.secrets import Secrets
import requests

#Clase que genera la comunicación directa con las IAs

class AIClient:

    #Inicialización del modelo principal Gemini

    gia.configure(api_key=Secrets.GIA_API_KEY)
    _model = gia.GenerativeModel("gemini-2.0-flash")
    

    #Función que hace llegar un prompt a Gemini y recoge su respuesta
    def askGemini(prompt: str):
        return AIClient._model.generate_content(prompt).text


    #Función que hace llegar un prompt a DeepSeek y recoge su respuesta
    def askDeepSeek(prompt: str):
        api_key = Secrets.DEEP_API_KEY
        api_url = "https://api.deepseek.com/v1/chat/completions"
        sesion = Session()

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 70,
            "temperature": 1,
            "stream": False
        }

        response = sesion.post(api_url, headers=headers, json=data, timeout=15)

        if response.status_code == 200:
            result = response.json()
            result = result["choices"][0]["message"]["content"]

            sesion.close()
            return result
        else:
            return "Error en la solicitud a la API."

    #Función que hace llegar un prompt a OpenAI y recoge su respuesta
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

        return completion.choices[0].message.content

    #Función que hace llegar un prompt a LlamaAI y recoge su respuesta
    def askLlamaAI(prompt: str):
        client = OpenAI(
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
    