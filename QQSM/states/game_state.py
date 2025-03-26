import reflex as rx
from QQSM.pages.Game import Game
import random

class GameState(rx.State):

    # Variables del juego
    question: str = "Presiona el botón para generar una pregunta"
    option_a: str = ""
    option_b: str = ""
    option_c: str = ""
    option_d: str = ""
    correct: str = ""
    number_question: int = 1
    topic: str = ""
    difficulty: int = 0
    feedback: str = ""
    fifty_used: bool = False
    public_used: bool = False
    call_used: bool = False
    public_stats: list[int] = []
    call_text: str = ""
    chosen_answer: bool = False
    correct_answer: bool = False

    # Estilos dinámicos de los botones
    button_classes: dict[str, str] = {
        "A": "custom-button",
        "B": "custom-button",
        "C": "custom-button",
        "D": "custom-button",
    }

    @rx.event
    def initialize_game(self):
        self.fifty_used = False
        self.public_used = False
        self.call_used = False
        self.public_stats = []
        self.call_text = ""
        self.chosen_answer = False
        self.correct_answer = False
        self.number_question = 1
        self.difficulty = 0
        self.generate_question()
        self.button_classes = {
            "A": "custom-button",
            "B": "custom-button",
            "C": "custom-button",
            "D": "custom-button",
        }
        return rx.redirect("/game")

    @rx.event
    def generate_question(self):
        """Genera una nueva pregunta usando Game."""
        game = Game(number_question=self.number_question)  
        topic = game.generate_topic(self.topic)
        difficulty = game.generate_difficulty_normal_mode(self.number_question)
        new_question = game.generate_question(difficulty, topic)

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
            "A": "custom-button",
            "B": "custom-button",
            "C": "custom-button",
            "D": "custom-button",
        }

        if self.number_question == 15:
            self.feedback = "¡Enhorabuena! ¡Has contestado correctamente a todas las preguntas!"
        else:
            self.number_question += 1
            self.generate_question()


    @rx.event
    def validate_answer(self, letter: str):
        """Valida la respuesta y actualiza los colores de los botones."""
        self.chosen_answer = True
        selected_option = getattr(self, f"option_{letter.lower()}")

        if selected_option == self.correct:
            self.correct_answer = True
            #self.feedback = "✅ ¡Correcto!" Los botones suplen este feedback
            self.button_classes[letter] = "custom-button success"
        else:
            self.correct_answer = False
            #self.feedback = "❌ ¡Incorrecto!" Los botones suplen este feedback
            self.button_classes[letter] = "custom-button error"

        for key in ["A", "B", "C", "D"]:
            if getattr(self, f"option_{key.lower()}") == self.correct:
                self.button_classes[key] = "custom-button success"


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
                self.button_classes[op] = "custom-button disabled"

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
                        self.public_stats.append({porcentaje})
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

