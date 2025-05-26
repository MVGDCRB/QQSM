import asyncio
from requests import Session
from openai import OpenAI
import google.generativeai as gia
from QQSM.secrets import Secrets
import requests
from typing import Any, Dict
import time, random

#Clase que genera la comunicación directa con las IAs

class AIClient:

    #Inicialización del modelo principal Gemini

    gia.configure(api_key=Secrets.GIA_API_KEY)
    _model = gia.GenerativeModel("gemini-2.0-flash")
    

    #Función que hace llegar un prompt a Gemini y recoge su respuesta
    def askGemini(prompt: str)-> str:
        return AIClient._model.generate_content(prompt).text


    #Función que hace llegar un prompt a DeepSeek y recoge su respuesta
    def askDeepSeek(prompt: str)-> str:
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
    def askOpenAI(prompt: str)-> str:
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
    def askLlamaAI(prompt: str) -> str:
        url = "https://api.llmapi.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {Secrets.LLAMA_API_KEY}",
            "Content-Type": "application/json",
        }

        # Prepara los mensajes y parámetros
        clean_prompt = prompt.strip().replace("\t", " ")
        payload: Dict[str, Any] = {
            "model": "llama4-maverick",
            "messages": [
                {"role": "system", "content": "Eres un asistente útil y conciso."},
                {"role": "user",   "content": clean_prompt}
            ],
            "max_tokens": 256,
            "temperature": 0.7,
            "top_p": 0.9,
            "n": 1,
            "stop": ["\n\n"]
        }

        # Retry en 422 con jitter
        for intento in range(2):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            except requests.HTTPError as e:
                code = resp.status_code if 'resp' in locals() else None
                body = resp.text if 'resp' in locals() else str(e)
                print(f"Intento {intento+1} fallido ({code}): {body}")
                if code == 422 and intento == 0:
                    time.sleep(0.2 + random.random() * 0.1)
                    continue
                raise RuntimeError(f"llamaAPI fallo {code}:\n{body}") from e

