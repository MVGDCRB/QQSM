import reflex as rx
from QQSM.pages.Game import Game

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
    public_stats: str = ""
    chosen_answer: bool = False
    correct_answer: bool = False


    @rx.event
    def initialize_game(self):
        self.fifty_used = False
        self.public_used = False
        self.public_stats = ""
        self.chosen_answer = False
        self.correct_answer = False
        self.number_question = 1
        self.difficulty = 0
        self.generate_question()
        return rx.redirect("/game")

    @rx.event
    def generate_question(self):
        """Genera una nueva pregunta usando Game."""
        game = Game(number_question=self.number_question)  
        topic = game.generate_topic()
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
        self.public_stats = ""
        

    @rx.event
    def next_round(self):
        self.chosen_answer = False
        self.correct_answer = False
        if self.number_question == 15:
            self.feedback = "¡Enhorabuena! ¡Has contestado correctamente a todas las preguntas!"
        else:
            self.number_question += 1
            self.generate_question()

    @rx.event
    def validate_answer(self, option: str):
        """Valida la respuesta usando la lógica de Game."""
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
        
        self.chosen_answer = True
        self.correct_answer = game.validate_question(option)

        if self.correct_answer:  # Si la respuesta es correcta
            self.feedback = "✅ ¡Correcto!"
        else:
            self.feedback = "❌ ¡Incorrecto!"
    @rx.event
    def use_fifty_option(self):
        """Usa el comodín 50:50 para eliminar dos respuestas incorrectas."""
        if not self.fifty_used:
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

            game.fifty_option()  # Llama a la función de Game

            # Actualiza las opciones después del 50:50
            self.option_a = game.option_a
            self.option_b = game.option_b
            self.option_c = game.option_c
            self.option_d = game.option_d
            self.fifty_used = True
        else:
            self.feedback = "❌ Ya has usado el comodín 50:50."

    @rx.event
    def use_public_option(self):
        """Usa el comodín del público y muestra las estadísticas."""
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

            stats = game.public_option()  # Llama a la función de Game

            if isinstance(stats, list):
                self.public_stats = "\n".join(stats)  # Convierte la lista en texto
            else:
                self.public_stats = stats  # En caso de que ya se haya usado

            self.public_used = True
        else:
            self.feedback = "❌ Ya has usado el comodín del público."    
