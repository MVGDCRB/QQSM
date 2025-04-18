import reflex as rx
from QQSM.pages.Game import Game
import random


class GameState(rx.State):

    # Variables del juego
    question: str = "Presiona un tema para generar una pregunta"
    option_a: str = ""
    option_b: str = ""
    option_c: str = ""
    option_d: str = ""
    correct: str = ""
    number_question: int = 1
    topic: str = ""
    topic_selection1: str = ""
    topic_selection2: str = ""
    difficulty: int = 0
    feedback: str = ""
    fifty_used: bool = False
    public_used: bool = False
    call_used: bool = False
    public_stats: list[int] = []
    call_text: str = ""
    chosen_answer: bool = False
    correct_answer: bool = False
    mode: str = ""
    enable_topic: bool = False
    game_class = ""

    # Estilos dinámicos de los botones
    button_classes: dict[str, str] = {
        "A": "hex-button",
        "B": "hex-button",
        "C": "hex-button",
        "D": "hex-button",
    }

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
        return rx.redirect(self.mode)

    @rx.event
    def set_theme(self, topic: str):
        self.chosen_answer = False
        self.enable_topic = True
        self.topic = topic
        new_question = self.game_class.generate_question(self.difficulty, self.topic)
        self.question = new_question[0]
        self.option_a = new_question[1]
        self.option_b = new_question[2]
        self.option_c = new_question[3]
        self.option_d = new_question[4]
        self.correct = new_question[5]

    @rx.event
    def get_themes(self):
        self.topic_selection1, self.topic_selection2 = self.game_class.generate_topic_theme_mode(self.topic_selection1,
                                                                                                 self.topic_selection2)

    @rx.event
    def empty_question(self):
        self.chosen_answer = True
        return ["Presiona un tema para generar una pregunta", "", "", "", "", ""]

    @rx.event
    def generate_question(self):
        """Genera una nueva pregunta usando Game."""
        self.game_class = Game(number_question=self.number_question)
        topic = ""
        if self.mode == "/theme":
            self.get_themes()
        else:
            topic = self.game_class.generate_topic_normal_mode(self.topic)

        if self.mode == "/game":
            difficulty = self.game_class.generate_difficulty_normal_mode(self.number_question)
            new_question = self.game_class.generate_question(difficulty, topic)
        elif self.mode == "/endless":
            difficulty = self.game_class.generate_difficulty_endless_mode()
            new_question = self.game_class.generate_question(difficulty, topic)
        else:
            difficulty = self.game_class.generate_difficulty_normal_mode(self.number_question)
            new_question = self.empty_question()

        # Actualiza el estado con la nueva pregunta
        self.question = new_question[0]
        self.option_a = new_question[1]
        self.option_b = new_question[2]
        self.option_c = new_question[3]
        self.option_d = new_question[4]
        self.correct = new_question[5]
        self.topic = topic
        self.difficulty = difficulty
        self.feedback = ""
        self.public_stats = []
        self.call_text = ""

    @rx.event
    def next_round(self):
        self.chosen_answer = False
        self.correct_answer = False
        self.feedback = ""

        # Resetear estilos de los botones
        self.button_classes = {
            "A": "hex-button",
            "B": "hex-button",
            "C": "hex-button",
            "D": "hex-button",
        }

        if self.number_question == 15 and (self.mode == "/game" or self.mode == "/theme"):
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
            # self.feedback = "✅ ¡Correcto!" Los botones suplen este feedback
            self.button_classes[letter] = "hex-button success"
        else:
            self.correct_answer = False
            # self.feedback = "❌ ¡Incorrecto!" Los botones suplen este feedback
            self.button_classes[letter] = "hex-button error"

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

            # Marcar los botones eliminados como incorrectos en rojo
            for op in eliminadas:
                self.button_classes[op] = "hex-button disabled"

            self.fifty_used = True
        else:
            self.feedback = "❌ Ya has usado el comodín 50:50."

    @rx.event
    def use_public_option(self):
        """Usa el comodín del público y guarda los porcentajes como lista de tuplas."""
        if not self.public_used:
            game = Game(
                question=self.question,
                option_a=self.option_a,
                option_b=self.option_b,
                option_c=self.option_c,
                option_d=self.option_d,
                correct=self.correct,
                number_question=self.number_question,
                difficulty=self.difficulty,
                topic=self.topic
            )

            stats = game.public_option()

            if isinstance(stats, list):
                self.public_stats = []
                for item in stats:
                    try:
                        texto, porcentaje = item.split(":", 1)
                        porcentaje = int(porcentaje.replace("%", "").strip())
                        self.public_stats.append(porcentaje)
                    except Exception as e:
                        print(f"Error al parsear resultado del público: {e}")
            else:
                self.feedback = stats  # En caso de error, muestra el texto devuelto como feedback        

            self.public_used = True
        else:
            self.feedback = "❌ Ya has usado el comodín del público."

    @rx.event
    def use_call_option(self):
        """Usa el comodín de la llamada y muestra un texto."""
        if not self.call_used:
            game = Game(
                question=self.question,
                option_a=self.option_a,
                option_b=self.option_b,
                option_c=self.option_c,
                option_d=self.option_d,
                correct=self.correct,
                number_question=self.number_question,
                difficulty=self.difficulty,
                topic=self.topic
            )

            text = game.call_option()  # Obtiene el texto de la llamada
            self.call_text = "\n La opcion correcta es " + text[0] + ". " + text[1]
            self.call_used = True
        else:
            self.feedback = "❌ Ya has usado el comodín de la llamada."
