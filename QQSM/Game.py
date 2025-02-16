import google.generativeai as gia
import random


class Game:
    gia.configure(api_key="AIzaSyDpS75LFcrsDFQz1UTLnX1Dfr-W9P-EgAI")  # Reemplaza con tu clave de API
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

    def generate_question(self, difficulty, topic):
        question = ("quiero que me hagas una pregunta como si fuera quien quiere ser millonario con una dificultad " +
                    str(difficulty) + "/100 y que el tema de la pregunta sea " + topic +
                    ". Tambien quiero que el formato este separado por punto y coma donde me muestre la pregunta las cuatro respuestas y la pregunta correcta.Como ejemplo ;Pregunta:;¿cual es la capital de España?;Paris;Roma;Madrid;Wansinton;Madrid; Pasame solo el mensaje sin nada extra")
        answer = self._model.generate_content(question).text
        answer = answer.split(";")
        if answer[0] == " ":
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

    def generate_topic(self):
        random_topic = random.choice(self.topics)
        while random_topic == self.topic:
            random_topic = random.choice(self.topics)
        return random_topic
