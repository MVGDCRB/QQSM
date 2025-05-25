import reflex as rx
from QQSM.states.login_state import LoginState
from QQSM.auth import update_user_stats, update_max_score
from QQSM.ai_client import AIClient
from openai import OpenAI
from QQSM.secrets import Secrets
import random
import re



class GameState(LoginState):

    # Variables del juego
    question: str = "Presiona un tema para generar una pregunta"

    option_a: str = "" 
    option_b: str = ""
    option_c: str = ""
    option_d: str = ""

    correct: str = ""
    chosen_answer: bool = False
    correct_answer: bool = False

    number_question: int = 1

    topics = ["arte", "fisica", "historia", "quimica", "musica", "matematicas",
                       "literatura", "biologia", "historia de la television", "videojuegos",
                       "moda", "tecnologia", "cocina", "deportes", "geografia"]
    topic: str = ""
    topic_selection1: str = ""
    topic_selection2: str = ""
    enable_topic: bool = False

    difficulties_NM = [5, 12, 20, 30, 38, 45, 52, 60, 68, 75, 80, 85, 90, 95, 100]
    difficulty: int = 0

    feedback: str = ""

    fifty_used: bool = False
    public_used: bool = False
    call_used: bool = False

    public_stats: list[int] = []
    public_items: list[tuple[str, int]] = []

    call_text: str = ""
    text_answer: str = ""

    mode: str = ""
    
    _model = None

    rival: str = ""

    # Estilos dinámicos de los botones
    button_classes: dict[str, str] = {}

    @rx.event
    def initialize_game(self, ruta: str):
        self.fifty_used = False
        self.public_used = False
        self.call_used = False
        self.public_stats = []
        self.call_text = ""
        self.chosen_answer = False
        self.correct_answer = False
        self.number_question = 1
        self.difficulty = 0
        self.button_classes = {
            "A": "hex-button",
            "B": "hex-button",
            "C": "hex-button",
            "D": "hex-button",
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

    @rx.event
    def set_theme(self, topic):
        self.topic = topic
        self.chosen_answer = False
        self.enable_topic = True
        new_question = self.getAIanswer()
        self.question = new_question[0]
        self.option_a = new_question[1]
        self.option_b = new_question[2]
        self.option_c = new_question[3]
        self.option_d = new_question[4]
        self.correct = new_question[5]

    @rx.event
    def get_themes(self):
        self.topic_selection1, self.topic_selection2 = self.generate_topic_theme_mode()

    @rx.event
    def empty_question(self):
        self.chosen_answer = True
        return ["Presiona un tema para generar una pregunta", "", "", "", "", ""]


    @rx.event
    def next_round(self):
        self.chosen_answer = False
        self.correct_answer = False
        self.feedback = ""
        self.call_text = ""
        self.public_stats = []
        self.public_items = []

        self.button_classes = {
            "A": "hex-button",
            "B": "hex-button",
            "C": "hex-button",
            "D": "hex-button",
        }

        if self.number_question == 15 and self.mode in ["/deepSeekIA", "/openAI", "/llamaIA", "/game", "/theme"]:
            self.feedback = "¡Enhorabuena! ¡Has contestado correctamente a todas las preguntas!"
        else:
            self.number_question += 1
            self.enable_topic = False
            self.generate_question()

    @rx.event
    def validate_answer(self, letter: str):
        """Valida la respuesta y actualiza los colores de los botones."""
        self.chosen_answer = True
        selected_option = getattr(self, f"option_{letter.lower()}")

        if selected_option == self.correct:
            self.correct_answer = True
            self.button_classes[letter] = "hex-button success"

        else:
            self.correct_answer = False
            self.button_classes[letter] = "hex-button error"
        
        if self.mode in ["/game", "/theme", "/endless"]:
            # Se actualizan las stats de usuario
            update_max_score(self.username, self.number_question*10)
            update_user_stats(self.username, self.topic, self.correct_answer)

        for key in ["A", "B", "C", "D"]:
            if getattr(self, f"option_{key.lower()}") == self.correct:
                self.button_classes[key] = "hex-button success"

    @rx.event
    def use_fifty_option(self):
        """Usa el comodín 50:50 para marcar dos respuestas incorrectas como erróneas."""
        if not self.fifty_used:
            opciones = ["A", "B", "C", "D"]
            incorrectas = [op for op in opciones if getattr(self, f"option_{op.lower()}") != self.correct]

            # Seleccionar dos opciones incorrectas al azar
            eliminadas = random.sample(incorrectas, 2)

            # Marcar los botones eliminados como incorrectos en gris
            for op in eliminadas:
                self.button_classes[op] = "hex-button disabled"

            self.fifty_used = True
        else:
            self.feedback = "❌ Ya has usado el comodín 50:50."

    @rx.event
    def use_public_option(self):
        """Usa el comodín del público y guarda los porcentajes como lista de tuplas."""
        if self.public_used:
            self.feedback = "❌ Ya has usado el comodín del público."
            return

        stats = self.askPublic()

        if isinstance(stats, str):
            # Mensaje de error
            self.feedback = stats
        else:
            # Unir trozos para obtener el texto íntegro
            full_text = ";".join(stats)
            # Extraer todos los números antes de '%'
            nums = re.findall(r"(\d+)%", full_text)

            percentages = [int(n) for n in nums]

            # Guardar en public_stats
            self.public_stats = percentages

            # Mapear letras A–D a cada porcentaje
            letters = ["A", "B", "C", "D"]
            self.public_items = [
                (letters[i], percentages[i])
                for i in range(min(len(letters), len(percentages)))
            ]

        self.public_used = True


    


    @rx.event
    def use_call_option(self):
        if not self.call_used:
            self.call_used = True
            self.call_text = ""
            
            message = (
                "En '¿Quién quiere ser millonario?', la pregunta es: " + self.question +
                "Opciones: " + self.option_a + ", " + self.option_b + ", " + self.option_c + ", " + self.option_d + "."
                + "Usando el comodín de la llamada, muestra solo con el siguiente formato: "
                  "respuesta correcta;descripcion breve."
            )

            text = AIClient.callGemini(message)

            self.call_text = "\n La opcion correcta es " + text[0] + ". " + text[1]
            self.call_used = True
        else:
            self.feedback = "❌ Ya has usado el comodín de la llamada."
        


    @rx.event
    def deep_seek_answer(self):
        """Mostrar la respuesta de DeepSeek."""
        print("DeepSeek Answer (game_state.py)")
        
        
        message = (
            "Responde a la pregunta: " + self.question +
            "Opciones: " + self.option_a + ", " + self.option_b + ", " + self.option_c + ", " + self.option_d + "."
            + "Muestrame SOLO LA LETRA de la solucion, ni ningun efecto, ni ningun caracter especial, "
            "solo la letra. Opciones: A, B, C, D. "
        )

        answer = AIClient.askDeepSeek(message)

        print(answer)
        return answer  # Devuelve la respuesta para su uso posterior   
        

    @rx.event
    def openai_answer(self):
        """Mostrar la respuesta de OpenAI."""
        print("OpenAI Answer (game_state.py)")

        message = ("Responde a la pregunta: " + self.question +
                            "Opciones: " + self.option_a + ", " + self.option_b + ", " + self.option_c + ", "
                            + self.option_d + "." + "Muestrame SOLO LA LETRA de la solucion, sin negrita "
                                                    "ni ningun efecto, ni ningun caracter especial, "
                                                    "solo la letra. Opciones: A, B, C, D."
        )

        answer = AIClient.askOpenAI(message)

        print(answer)
        return answer  # Devuelve la respuesta para su uso posterior        
    

    


    @rx.event
    def llama_answer(self):
        """Mostrar la respuesta de LlamaIA."""
        print("LlamaIA Answer (game_state.py)")
       
        
        message = ("Responde a la pregunta: " + self.question +
                               "Opciones: " + self.option_a + ", " + self.option_b + ", " + self.option_c + ", " +
                               self.option_d + "." + "Muestrame SOLO LA LETRA de la solucion, sin negrita "
                                                     "ni ningun efecto, ni ningun caracter especial, "
                                                     "solo la letra. Opciones: A, B, C, D."
        )
        answer = AIClient.askLlamaAI(message)
        
        print(answer)
        return answer  # Devuelve la respuesta para su uso posterior
    
    @rx.event
    def generate_question(self):
        """Genera una nueva pregunta"""

        # Primero se generan los temas en funcion de si hacen falta 1 o 2
        if self.mode == "/theme":
            self.get_themes()
        else:
            self.topic = self.generate_topic_normal_mode()

        # Despues se genera la dificultad y la pregunta en funcion del modo de juego
        if self.mode in ["/deepSeekIA", "/openAI", "/llamaIA", "/game"]:
            difficulty = self.generate_difficulty_normal_mode()
            new_question = self.getAIanswer()
        elif self.mode == "/endless":
            difficulty = self.generate_difficulty_endless_mode()
            new_question = self.getAIanswer()
        else:
            difficulty = self.generate_difficulty_normal_mode()
            new_question = self.empty_question()

        # Actualiza el estado con la nueva pregunta
        self.question = new_question[0]
        self.option_a = new_question[1]
        self.option_b = new_question[2]
        self.option_c = new_question[3]
        self.option_d = new_question[4]
        self.correct = new_question[5]
        self.difficulty = difficulty
        self.feedback = ""
        self.public_stats = []
        self.call_text = ""

        if self.mode == "/deepSeekIA":
            answer = self.deep_seek_answer()
            self.validate_answer(answer)
        elif self.mode == "/openAI":
            answer = self.openai_answer()
            self.validate_answer(answer)
        elif self.mode == "/llamaIA":
            answer = self.llama_answer()
            self.validate_answer(answer)

    def getAIanswer(self):
        question = ("Quiero que me hagas una pregunta como si fuera quien quiere ser millonario con una dificultad " +
                    str(self.difficulty) + "/100 y que el tema de la pregunta sea " + self.topic +
                    ". Tambien quiero que el formato este separado por punto y coma donde me muestre la pregunta las "
                    "cuatro respuestas y la pregunta correcta.Como ejemplo Pregunta:;¿cual es la capital de "
                    "España?;Paris;Roma;Madrid;Wansinton;Madrid; Pasame solo el mensaje sin nada extra")
        answer = AIClient.askAI(question)
        answer = answer.split(";")
        if answer[0] == " " or answer[0] == "":
            del answer[0]
        del answer[0]
        if answer[-1] == "\n":
            del answer[-1]
        answer[-1] = answer[-1].replace("\n", "")
        return answer

    def generate_difficulty_normal_mode(self):
        return self.difficulties_NM[self.number_question - 1]

    def generate_difficulty_endless_mode(self):
        if 4 * self.number_question < 100:
            return 4 * self.number_question
        else:
            return 100

    def generate_topic_normal_mode(self):
        random_topic = random.choice(self.topics)
        if self.topic != "":
            while random_topic == self.topic:
                random_topic = random.choice(self.topics)
        return random_topic

    def generate_topic_theme_mode(self):
        # Si los anteriores eran válidos, no repetirlos
        topic1,topic2 = self.topic_selection1, self.topic_selection2
        prev_topics = {topic1, topic2} if topic1 != "" and topic2 != "" and topic1 != topic2 else set()

        # Elegir dos nuevos temas diferentes entre sí y diferentes de los anteriores
        topics_left = [t for t in self.topics if t not in prev_topics]

        return random.sample(topics_left, 2)

    def validate_question(self, option):
        next_question = False
        if option == self.correct:
            self.number_question += 1
            next_question = True
        return next_question

    def askPublic(self):
        if not self.public_used:
            public = ("Estoy jugando a quien quiere ser millonario y me preguntan" + self.question +
                      "con estas posibles respuestas" + self.option_a + self.option_b + self.option_c + self.option_d +
                      "y quiero usar el comodin del publico. Quero que solo me muestres el texto del comodin del "
                      "publico de la siguiente forma como en el ejemplo : "
                      "Courrèges:15%;Miyake:60%;Ungaro:5%Cardin:20% .Pasame solo el mensaje sin nada extra ")
            statistics = AIClient.askAI(public)
            statistics = statistics.split(";")
            if statistics[-1] == "\n":
                del statistics[-1]
            statistics[-1] = statistics[-1].replace("\n", "")
            self.public_used = True
            return statistics
        else:
            return "No se puede usar el comodin porque ya ha sido usado"
        

