import google.generativeai as gia
import random
from requests import Session


class Game:
    gia.configure(api_key="AIzaSyAnGcswACvftlgtjbe8Rw747jncEtmgMo8")  # Reemplaza con tu clave de API
    _model = gia.GenerativeModel("gemini-2.0-flash")  # Especifica el modelo Gemini que quieres usar

    def __init__(self, question: str = "", option_a: str = "", option_b: str = "",
                 option_c: str = "", option_d: str = "", correct: str = "", number_question: int = 1,
                 difficulty: int = 0, topic: str = ""):
        self.question = question
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.correct = correct
        self.number_question = number_question
        self.difficulty = difficulty
        self.topic = topic
        self.difficulties_NM = [5, 12, 20, 30, 38, 45, 52, 60, 68, 75, 80, 85, 90, 95, 100]
        self.topics = ["arte", "fisica", "historia", "quimica", "musica", "matematicas",
                       "literatura", "biologia", "historia de la television", "videojuegos",
                       "moda", "tecnologia", "cocina", "deportes", "geografia"]
        self.fifty = 1
        self.public = 1
        self.call = 1

    def generate_question(self, difficulty, topic):
        question = ("Quiero que me hagas una pregunta como si fuera quien quiere ser millonario con una dificultad " +
                    str(difficulty) + "/100 y que el tema de la pregunta sea " + topic +
                    ". Tambien quiero que el formato este separado por punto y coma donde me muestre la pregunta las "
                    "cuatro respuestas y la pregunta correcta.Como ejemplo Pregunta:;¿cual es la capital de "
                    "España?;Paris;Roma;Madrid;Wansinton;Madrid; Pasame solo el mensaje sin nada extra")
        answer = self._model.generate_content(question).text
        answer = answer.split(";")
        if answer[0] == " " or answer[0] == "":
            del answer[0]
        del answer[0]
        if answer[-1] == "\n":
            del answer[-1]
        answer[-1] = answer[-1].replace("\n", "")
        return answer

    def set_question(self, answer, number_question: int, difficulty: int, topic: str):
        self.question = answer[0]
        self.option_a = answer[1]
        self.option_b = answer[2]
        self.option_c = answer[3]
        self.option_d = answer[4]
        self.correct = answer[5]
        self.number_question = number_question
        self.topic = topic
        self.difficulty = difficulty

    def generate_difficulty_normal_mode(self, number_question: int):
        return self.difficulties_NM[number_question - 1]

    def generate_difficulty_endless_mode(self):
        if 4 * self.number_question < 100:
            return 4 * self.number_question
        else:
            return 100

    def generate_topic_normal_mode(self, topic: str):
        random_topic = random.choice(self.topics)
        if topic != "":
            while random_topic == topic:
                random_topic = random.choice(self.topics)
        return random_topic

    def generate_topic_theme_mode(self, topic1: str, topic2: str):
        random_topic1 = random.choice(self.topics)
        random_topic2 = random.choice(self.topics)
        if topic1 != "" and topic2 != "":
            while ((random_topic1 == topic1 or random_topic2 == topic1) and
                   (random_topic1 == topic2 or random_topic2 == topic2) or
                   (topic1 == topic2)):
                random_topic1 = random.choice(self.topics)
                random_topic2 = random.choice(self.topics)
        return random_topic1, random_topic2

    def validate_question(self, option):
        next_question = False
        if option == self.correct:
            self.number_question += 1
            next_question = True
        return next_question

    def fifty_option(self):
        if self.fifty > 0:
            list_answer = [self.option_a, self.option_b, self.option_c, self.option_d]
            random_question = random.choice(list_answer)
            while random_question == self.correct:
                random_question = random.choice(list_answer)

            for answer in list_answer:
                if answer != random_question and answer != self.correct:
                    match answer:
                        case self.option_a:
                            self.option_a = ""
                        case self.option_b:
                            self.option_b = ""
                        case self.option_c:
                            self.option_c = ""
                        case self.option_d:
                            self.option_d = ""

            self.fifty -= 1
        else:
            return "No se puede usar el comodin porque ya ha sido usado"

    def public_option(self):
        if self.public > 0:
            public = ("Estoy jugando a quien quiere ser millonario y me preguntan" + self.question +
                      "con estas posibles respuestas" + self.option_a + self.option_b + self.option_c + self.option_d +
                      "y quiero usar el comodin del publico. Quero que solo me muestres el texto del comodin del "
                      "publico de la siguiente forma como en el ejemplo : "
                      "Courrèges:15%;Miyake:60%;Ungaro:5%Cardin:20% .Pasame solo el mensaje sin nada extra ")
            statistics = self._model.generate_content(public).text
            statistics = statistics.split(";")
            if statistics[-1] == "\n":
                del statistics[-1]
            statistics[-1] = statistics[-1].replace("\n", "")
            self.public -= 1
            return statistics
        else:
            return "No se puede usar el comodin porque ya ha sido usado"

    def call_option(self):
        if self.call > 0:
            api_key = "sk-0c4a68c97ce14b288ec1a6b5b9117e21"
            api_url = "https://api.deepseek.com/v1/chat/completions"  # Reemplaza con la URL correcta
            message = (
                "En '¿Quién quiere ser millonario?', la pregunta es: " + self.question +
                "Opciones: " + self.option_a + ", " + self.option_b + ", " + self.option_c + ", " + self.option_d + "."
                + "Usando el comodín de la llamada, muestra solo con el siguiente formato: "
                  "respuesta correcta;descripcion breve."
            )

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
                        "content": message  # El contenido del mensaje
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
                self.call -= 1
                sesion.close()
                return result
        else:
            return "No se puede usar el comodin porque ya ha sido usado"
