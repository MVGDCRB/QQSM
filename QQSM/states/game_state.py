import reflex as rx
from QQSM.states.login_state import LoginState
from QQSM.auth import update_user_stats, update_max_score, topics
from QQSM.ai_client import AIClient
from openai import OpenAI
from QQSM.secrets import Secrets
import random
import re


#Estado reflex de game_page que gestiona la lógica del juego

class GameState(LoginState):

    # Variables de gestión del juego

    #Enunciado de la pregunta
    question: str = "Presiona un tema para generar una pregunta"

    #Posibles respuestas a la pregunta
    option_a: str = ""
    option_b: str = ""
    option_c: str = ""
    option_d: str = ""

    #Respuesta correcta a la pregunta
    correct: str = ""

    #True si se ha elegido una respuesta
    chosen_answer: bool = False

    #True si se ha elegido la respuesta correcta
    correct_answer: bool = False

    #Índice de la pregunta actual
    number_question: int = 1
    
    #Tema de la pregunta actual
    topic: str = ""

    #Posibles temas a elegir en el modo temático
    topic_selection1: str = ""
    topic_selection2: str = ""

    #Se fija a True cuando se elige un tema
    enable_topic: bool = False

    #Niveles de dificultad parametrizados para el prompt de la IA
    difficulties_NM = [5, 12, 20, 30, 38, 45, 52, 60, 68, 75, 80, 85, 90, 95, 100]

    #Nivel de dificultad actual
    difficulty: int = 0

    #Campo de texto para mostrar al usuario en caso de error o información adicional
    feedback: str = ""

    #True cuando se consume cada uno de los posibles comodines
    fifty_used: bool = False
    public_used: bool = False
    call_used: bool = False

    #Lista que almacena las 4 respuestas posibles asociadas a su porcentaje de voto del público
    public_items: list[tuple[str, int]] = []

    #Texto generado por la IA que se muestra en el comodín de la llamada
    call_text: str = ""

    #Modo de juego actual
    mode: str = ""
    
    #IA rival cuando se está jugando el modo máquina VS máquina
    rival: str = ""

    # Estilos css dinámicos de los botones según validez de respuesta
    button_classes: dict[str, str] = {}

    #Función que inicializa las variables de estado según el modo de juego de una nueva partida
    @rx.event
    def initialize_game(self, ruta: str):
        self.fifty_used = False
        self.public_used = False
        self.call_used = False
        self.call_text = ""
        self.chosen_answer = False
        self.correct_answer = False
        self.number_question = 1
        self.difficulty = 0
        self.button_classes = {
            "A": "hex-button subheader-style",
            "B": "hex-button subheader-style",
            "C": "hex-button subheader-style",
            "D": "hex-button subheader-style",
        }
        self.enable_topic = False
        self.mode = ruta
        self.generate_question()
        
        if self.mode == "/deepSeekIA":
            self.rival = "deepSeek"
            return rx.redirect("/GeminiVS")

        elif self.mode == "/openAI":
            self.rival = "openAI"
            return rx.redirect("/GeminiVS")

        elif self.mode == "/llamaIA":
            self.rival = "llamaIA"
            return rx.redirect("/GeminiVS")

        return rx.redirect(self.mode)

    #Función que fija el tema elegido en el modo temático y genera la pregunta asociada a dicho tema
    @rx.event
    def set_theme(self, topic):
        if topic != self.topic:
            self.topic = topic
            self.chosen_answer = False
            self.enable_topic = True
            new_question = self.getAIanswer()
            if new_question and len(new_question) == 6:
                self.question = new_question[0]
                self.option_a = new_question[1]
                self.option_b = new_question[2]
                self.option_c = new_question[3]
                self.option_d = new_question[4]
                self.correct = new_question[5]
            else:
                self.handle_generation_error()

    #Función que recoge dos nuevos temas al azar para la siguiente elección del modo temático
    @rx.event
    def get_themes(self):
        self.topic_selection1, self.topic_selection2 = self.generate_topic_theme_mode()

    #Función que inicializa el estado de la pregunta en cada elección del modo temático
    @rx.event
    def empty_question(self):
        self.chosen_answer = True
        return ["Presiona un tema para generar una pregunta", "", "", "", "", ""]

    #Función que prepara el estado de las variables para la siguiente pregunta
    @rx.event
    def next_round(self):
        self.chosen_answer = False
        self.correct_answer = False
        self.feedback = ""
        self.call_text = ""
        self.public_items = []

        self.button_classes = {
            "A": "hex-button subheader-style",
            "B": "hex-button subheader-style",
            "C": "hex-button subheader-style",
            "D": "hex-button subheader-style",
        }

        if self.number_question == 15 and self.mode in ["/deepSeekIA", "/openAI", "/llamaIA", "/game", "/theme"]:
            self.feedback = "¡Enhorabuena! ¡Has contestado correctamente a todas las preguntas!"
        else:
            self.number_question += 1
            self.enable_topic = False
            self.generate_question()

    #Función que valida la respuesta dada a la pregunta y actualiza las clases .css de los botones de respuesta, así como las estadísticas del usuario
    @rx.event
    def validate_answer(self, letter: str):
        
        self.chosen_answer = True
        selected_option = getattr(self, f"option_{letter.lower()}")

        if selected_option == self.correct:
            self.correct_answer = True
            self.button_classes[letter] = "hex-button success"

        else:
            self.correct_answer = False
            self.button_classes[letter] = "hex-button error"
        
        if self.mode in ["/game", "/theme", "/endless"]:
            update_max_score(self.username, self.number_question*10)
            update_user_stats(self.username, self.topic, self.correct_answer)

        for key in ["A", "B", "C", "D"]:
            if getattr(self, f"option_{key.lower()}") == self.correct:
                self.button_classes[key] = "hex-button success"
            elif self.button_classes[key] == "hex-button subheader-style":
                self.button_classes[key] = "hex-button"

    #Función que actualiza el estado de los botones al usuar el comodín 50:50 deshabilitando dos de las opciones
    @rx.event
    def use_fifty_option(self):
        if not self.fifty_used:
            opciones = ["A", "B", "C", "D"]
            incorrectas = [op for op in opciones if getattr(self, f"option_{op.lower()}") != self.correct]

            eliminadas = random.sample(incorrectas, 2)

            for op in eliminadas:
                self.button_classes[op] = "hex-button disabled"

            self.fifty_used = True
        else:
            self.feedback = "❌ Ya has usado el comodín 50:50."

    #Función que actualiza el estado de los botones al usuar el comodín del público, generando el valor de public_items tras consultar a la IA
    @rx.event
    def use_public_option(self):
        if self.public_used:
            self.feedback = "❌ Ya has usado el comodín del público."
            return

        stats = self.askPublic()

        if isinstance(stats, str):
            self.feedback = stats
        else:
            full_text = ";".join(stats)
            nums = re.findall(r"(\d+)%", full_text)

            percentages = [int(n) for n in nums]

            letters = ["A", "B", "C", "D"]
            self.public_items = [
                (letters[i], percentages[i])
                for i in range(min(len(letters), len(percentages)))
            ]

        self.public_used = True


    #Función que actualiza el estado de los botones al usuar el comodín de la llamada, generando el valor de call_text tras consultar a la IA
    @rx.event
    def use_call_option(self):
        if not self.call_used:
            self.call_used = True
            self.call_text = ""
            
            message = (
                "Te llaman usando el comodín desde '¿Quién quiere ser millonario?', la pregunta es: " + self.question +
                "Opciones (A,B,C,D): " + self.option_a + ", " + self.option_b + ", " + self.option_c + ", " + self.option_d + "."
                + " muestra tu respuesta con el siguiente formato: "
                "Saludo simpático+La respuesta correcta es: letra)+opcion en negrita markdown+justificación breve y simpática de por qué es la opción correcta."
            )

            text = AIClient.askGemini(message)

            self.call_text = text
            self.call_used = True
        else:
            self.feedback = "❌ Ya has usado el comodín de la llamada."

    #Función auxiliar que dada la pregunta y opciones actuales construye un prompt para preguntar a cualquiera de las IAs para recibir una única letra (A,B,C,D) como respuesta
    def generate_question_prompt(self) -> str:
        return (
            f"Responde a la pregunta: {self.question} "
            f"Con una de las pciones (A, B, C, D): {self.option_a}, {self.option_b}, {self.option_c}, {self.option_d}. "
            "Muestrame SOLO LA LETRA de la solución, sin negrita ni ningún efecto, "
            "ni caracter especial, solo la letra(A, B, C o D)."
        )

    #Función que hace llegar la pregunta actual a DeepSeek y obtiene su respuesta en formato letra
    @rx.event
    def deep_seek_answer(self):
        prompt = self.generate_question_prompt()
        return self.safe_ai_call(lambda: AIClient.askDeepSeek(prompt))
        
    #Función que hace llegar la pregunta actual a OpenAI y obtiene su respuesta en formato letra
    @rx.event
    def openai_answer(self):
        prompt = self.generate_question_prompt()
        return self.safe_ai_call(lambda: AIClient.askOpenAI(prompt))
    
    #Función que hace llegar la pregunta actual a LLamaAI y obtiene su respuesta en formato letra
    @rx.event
    def llama_answer(self):
        prompt = self.generate_question_prompt()
        return self.safe_ai_call(lambda: AIClient.askLlamaAI(prompt))
    
    #Ejecuta la llamada a la ai call() capturando y manejando excepciones.
    def safe_ai_call(self, call) -> str:
        try:
            return call()
        except Exception as e:
            return self.handle_ai_error(e)
        
    #Maneja un posible error al llamar a la API de una IA a nivel interfaz
    def handle_ai_error(self, e:Exception):
        print("Error en AI call:", e)
        self.button_classes = {opt: "hex-button disabled" for opt in ("A", "B", "C", "D")}
        self.feedback = "Se produjo un error al llamar a la API de la IA rival"
        return None
    
    #Función que actualiza las variables de estado para generar una nueva pregunta según el modo de juego
    @rx.event
    def generate_question(self):

        # Generación de nuevo tema
        if self.mode == "/theme":
            self.get_themes()
        else:
            self.topic = self.generate_topic_normal_mode()

        # Generacion de dificultad y pregunta
        if self.mode in ["/deepSeekIA", "/openAI", "/llamaIA", "/game"]:
            difficulty = self.generate_difficulty_normal_mode()
            new_question = self.getAIanswer()
        elif self.mode == "/endless":
            difficulty = self.generate_difficulty_endless_mode()
            new_question = self.getAIanswer()
        else:
            difficulty = self.generate_difficulty_normal_mode()
            new_question = self.empty_question()

        if new_question and len(new_question) == 6:
                self.question = new_question[0]
                self.option_a = new_question[1]
                self.option_b = new_question[2]
                self.option_c = new_question[3]
                self.option_d = new_question[4]
                self.correct = new_question[5]

                self.difficulty = difficulty
                self.feedback = ""
                self.call_text = ""
                if self.mode == "/deepSeekIA":
                    answer = self.deep_seek_answer()
                    if answer:
                        self.validate_answer(answer)
                elif self.mode == "/openAI":
                    answer = self.openai_answer()
                    if answer:
                        self.validate_answer(answer)
                elif self.mode == "/llamaIA":
                    answer = self.llama_answer()
                    if answer:
                        self.validate_answer(answer)

        else:
                self.handle_generation_error()
        
    #Función que solicita a GeminiAI que genere una pregunta para el tema y dificultad actual y traduce la respuesta a un array con las opciones de respuesta y la respuesta correcta
    def getAIanswer(self):
        question = ("Debes generar una pregunta de concurso de cultura general."
                    "El porcentaje de dificultad de la pregunta es" + str(self.difficulty)+
                    "El tema de la pregunta es " + self.topic +
                    "El formato de la respuesta consta de 6 elementos, y solo 6, separados por ; "
                    "enunciado de la pregunta debe ir entre ¿?, cuatro respuestas no ambiguas, también concisas y la respuesta correcta."
                    "Evita que la respuesta o palabras similares aparezcan ya en el enunciado de la pregunta."
                    "No debes generar NINGÚN elemento adicional"
                    "Por ejemplo, para la pregunta:¿Cual es la capital de "
                    "España? y opciones (Paris, Roma, Madrid, Washington)"
                    "se devuelve: ¿Cual es la capital de España?;Paris;Roma;Madrid;Washington;Madrid")
        answer = AIClient.askGemini(question)
        answer = answer.strip().split(";")
        prompt_text = answer[0]
        match = re.search(r'¿[^?]*\?', prompt_text)
        if match:
            answer[0] = match.group(0)
        else:
            return None
        correct = answer[-1]
        if answer.count(correct) < 2:
            print(f"La respuesta correcta '{correct}' no está repetida en la lista {answer}")
            return None
        return answer
    
    #Función que actualiza el estado de la UI si se produce una generación incorrecta de la pregunta
    def handle_generation_error(self):
        self.chosen_answer  = True
        self.correct_answer = True
        self.feedback = "Se produjo un error interno al generar la pregunta"
        self.button_classes = {opt: "hex-button disabled" for opt in ("A", "B", "C", "D")}


    #Función que asigna la dificultad correspondiente al indice de la pregunta actual en el modo clásico
    def generate_difficulty_normal_mode(self):
        return self.difficulties_NM[self.number_question - 1]

    #Función que asigna la dificultad correspondiente al indice de la pregunta actual en el modo infinito
    def generate_difficulty_endless_mode(self):
        if 4 * self.number_question < 100:
            return 4 * self.number_question
        else:
            return 100

    #Función que genere un nuevo tema al azar para la siguiente pregunta del modo clásico sin repetir el anterior
    def generate_topic_normal_mode(self):
        random_topic = random.choice(topics)
        if self.topic != "":
            while random_topic == self.topic:
                random_topic = random.choice(topics)
        return random_topic

    #Función que genere dos nuevos temas al azar para la siguiente pregunta del modo temático sin repetir los anteriores
    def generate_topic_theme_mode(self):
        topic1,topic2 = self.topic_selection1, self.topic_selection2
        prev_topics = {topic1, topic2} if topic1 != "" and topic2 != "" and topic1 != topic2 else set()

        topics_left = [t for t in topics if t not in prev_topics]

        return random.sample(topics_left, 2)

    #Función que hace llegar a Gemini la pregunta actual para que genere las posibles respuestas del comodín del público en el formato array adecuado
    def askPublic(self):
            public = ("Estoy jugando a quien quiere ser millonario y me preguntan" + self.question +
                    "con estas posibles respuestas(A,B,C,D)" + self.option_a + self.option_b + self.option_c + self.option_d +
                    "y quiero usar el comodin del publico. Responde con el formato opcion:porcentaje; como en el ejemplo: "
                    "Courrèges:15%;Miyake:60%;Ungaro:5%;Cardin:20%.Pasame solo el mensaje sin nada extra ")
            statistics = AIClient.askGemini(public)
            statistics = statistics.split(";")
            if statistics[-1] == "\n":
                del statistics[-1]
            statistics[-1] = statistics[-1].replace("\n", "")
            self.public_used = True
            return statistics

