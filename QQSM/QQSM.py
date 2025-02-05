"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

import random


class State(rx.State):
    
    quiz_questions = [
    ("¿Cuál es la capital de Francia?", ["Madrid", "Berlín", "París", "Lisboa"], 2),
    ("¿Cuántos planetas hay en el sistema solar?", ["7", "8", "9", "10"], 1),
    ("¿Quién escribió 'Don Quijote de la Mancha'?", ["Cervantes", "Lorca", "Quevedo", "Góngora"], 0),
    ("¿Cuál es el resultado de 5 + 7?", ["10", "11", "12", "13"], 2),
    ("¿Qué gas respiramos principalmente?", ["Oxígeno", "Nitrógeno", "Dióxido de carbono", "Helio"], 0),
]

    totalPreguntas = len(quiz_questions)
    
    show_page_one: bool = True

    textoPregunta: str = None

    tituloOpciones: list[str] = ["A)", "B)", "C)", "D)"]

    textoOpciones: list[str] = []

    opcionCorrecta: int = -1

    numAcertadas: int = 0

    def toggle_page(self):
        self.show_page_one = not self.show_page_one

    def seleccionarPreguntaAleatoria(self):
        self.textoPregunta, self.textoOpciones, self.opcionCorrecta = random.choice(self.quiz_questions)

    def verificar_respuesta(self, seleccion: int):
        if seleccion == self.opcionCorrecta:
            print("✅ Respuesta correcta")
            self.numAcertadas = self.numAcertadas + 1
            rx.toast(
                "✅ Respuesta correcta",
                description="Cargando nueva pregunta...",
                duration=1500,  # Se muestra por 1.5 segundos
            )
            if self.numAcertadas == self.totalPreguntas:
                self.numAcertadas = 0
                self.toggle_page()
            else:
                self.seleccionarPreguntaAleatoria()  # ✅ Nueva pregunta después del toast
        else:
            print("❌ Respuesta incorrecta")
            rx.toast(
                "❌ Respuesta incorrecta",
                description="Regresando a la página anterior...",
                duration=1500,
            )
            self.toggle_page()  # ✅ Cambia de página después del toast


def index() -> rx.Component:
    return rx.cond(State.show_page_one, page_one(), page_two())

def page_one():
    return rx.center(
        rx.vstack(
            rx.text("Bienvenido a QQSM", font_size="2em"),
            rx.button("Comenzar", on_click=[
                State.toggle_page,
                State.seleccionarPreguntaAleatoria
            ]
                
                )

        )
    )

def page_two():
    return rx.center(
        rx.vstack(
            rx.text(State.textoPregunta, font_size="2em"),
            rx.hstack(
                *[
                    rx.button(
                        State.tituloOpciones[i] + " " + State.textoOpciones[i],  # Texto del botón
                        width="150px",
                        height="80px",
                        border="1px solid black",
                        padding="10px",
                        margin="5px",
                        align="center",
                        on_click=lambda i=i: State.verificar_respuesta(i),  # Llama a una función con el índice
                    )
                    for i in range(4)
                ]
            ),
            rx.text(f"Aciertos: {State.numAcertadas} / {State.totalPreguntas}", font_size="1.5em", color="blue"),  # ✅ Mostramos el contador          
        )
    )

app = rx.App()
app.add_page(index)
