import reflex as rx

@rx.page(route="/game")  # Registra la página en Reflex
def game_page():
    return rx.center(
        rx.text("🎮 Quién Quiere Ser Millonario", font_size="2em", font_weight="bold")
    )


"""from asyncio import timeout

import reflex as rx
# from QQSM.state import State
import google.generativeai as gia
from IPython.core.debugger import prompt
from prompt_toolkit.utils import to_str

gia.configure(api_key="AIzaSyDpS75LFcrsDFQz1UTLnX1Dfr-W9P-EgAI")  # Reemplaza con tu clave de API
model = gia.GenerativeModel("gemini-2.0-flash") # Especifica el modelo Gemini que quieres usar
"""
# from docutils.nodes import topic

"""
def game_page():
    return rx.cond(State.show_page_one, page_one(), page_two())


def page_one():
    return rx.center(
        rx.vstack(
            rx.text("Bienvenido a QQSM", font_size="2em"),
            rx.button("Comenzar", on_click=[State.toggle_page, State.seleccionarPregunta])
        )
    )


def page_two():
    return rx.center(
        rx.vstack(
            rx.text(State.textoPregunta, font_size="2em"),
            rx.hstack(
                *[
                    rx.button(
                        State.tituloOpciones[i] + " " + State.textoOpciones[i],
                        width="150px",
                        height="80px",
                        border="1px solid black",
                        padding="10px",
                        margin="5px",
                        align="center",
                        on_click=lambda i=i: State.verificar_respuesta(i),
                    )
                    for i in range(4)
                ]
            ),
            rx.text(f"Ronda: {State.numRonda} / {State.totalPreguntas}", font_size="1.5em", color="blue"),
        )
    )
"""

"""
def game_page():
    return rx.cond()
"""

"""
def generate_question(tema:str ="arte", dificultad:int=50):
    pregunta = "quiero que me hagas una pregunta como si fuera quien quiere ser millonario con una dificultad "+str(dificultad)+"/100 y que el tema de la pregunta sea "+tema+". Tambien quiero que el formato este separado por punto y coma donde me muestre la pregunta las cuatro respuestas y la pregunta correcta.Como ejemplo ;Pregunta:;¿cual es la capital de España?;Paris;Roma;Madrid;Wansinton;Madrid; Pasame solo el mensaje sin nada extra"
    respuesta = model.generate_content(pregunta).text
    print(f"Pregunta: {pregunta}")
    print(f"Respuesta: {respuesta}")
    return respuesta


question = generate_question()
question = question.split(";")
if question[0] == " ":
    del question[0]
del question[0]
if question[-1] == "\n":
    del question[-1]
question[-1] = question[-1].replace("\n", "")

print(question)
"""

"""from QQSM.pages.Game import Game

quiz = Game(number_question=1)
n_question = 15
topic_quiz = quiz.generate_topic()
difficulty_quiz = quiz.generate_difficulty_normal_mode(n_question)
question_quiz = quiz.generate_question(difficulty_quiz, topic_quiz)
quiz.set_question(question_quiz, n_question, difficulty_quiz, topic_quiz)
print(quiz.question, "\n", quiz.option_a, "\n", quiz.option_b, "\n", quiz.option_c, "\n", quiz.option_d, "\n",
      quiz.correct)
print(quiz.public_option())
quiz.fifty_option()
print(" X: ", quiz.option_a, "\n", "X: ", quiz.option_b, "\n", "X: ", quiz.option_c, "\n", "X: ", quiz.option_d, "\n")
"""