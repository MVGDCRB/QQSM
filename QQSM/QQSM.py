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
    ("¿En qué continente se encuentra Egipto?", ["Asia", "África", "Europa", "América"], 1),
    ("¿Cuántos lados tiene un hexágono?", ["4", "5", "6", "7"], 2),
    ("¿Qué país tiene la mayor población del mundo?", ["India", "Estados Unidos", "China", "Brasil"], 2),
    ("¿Quién pintó la Mona Lisa?", ["Van Gogh", "Picasso", "Da Vinci", "Rembrandt"], 2),
    ("¿Cuál es el metal más abundante en la corteza terrestre?", ["Hierro", "Aluminio", "Cobre", "Plata"], 1),
    ("¿En qué año llegó el hombre a la Luna?", ["1965", "1969", "1972", "1980"], 1),
    ("¿Cómo se llama el proceso por el cual las plantas producen oxígeno?", ["Respiración", "Fotosíntesis", "Fermentación", "Digestión"], 1),
    ("¿Qué instrumento mide la presión atmosférica?", ["Termómetro", "Barómetro", "Higrómetro", "Altímetro"], 1),
    ("¿Cuál es el país más grande del mundo por superficie?", ["Canadá", "Estados Unidos", "Rusia", "China"], 2),
    ("¿Qué escritor creó el personaje de Sherlock Holmes?", ["Agatha Christie", "J.K. Rowling", "Arthur Conan Doyle", "Edgar Allan Poe"], 2),
]

    totalPreguntas = len(quiz_questions)
    
    show_page_one: bool = True

    textoPregunta: str = None

    tituloOpciones: list[str] = ["A)", "B)", "C)", "D)"]

    textoOpciones: list[str] = []

    opcionCorrecta: int = -1

    numRonda: int = 1

    def toggle_page(self): # Provisional, para decidir si se muestra la pagina de inicio o la de preguntas
        self.show_page_one = not self.show_page_one

    def seleccionarPregunta(self): #Coge la pregunta que toque
        self.textoPregunta, self.textoOpciones, self.opcionCorrecta = self.quiz_questions[self.numRonda-1]

    def verificar_respuesta(self, seleccion: int): #Vuelve al principio si se ha fallado o sigue con la siguiente
        if seleccion == self.opcionCorrecta:
            print("✅ Respuesta correcta")
            self.numRonda = self.numRonda + 1
           
            if self.numRonda == self.totalPreguntas:
                self.numRonda = 1
                self.toggle_page()
            else:
                self.seleccionarPregunta()  
        else:
            print("❌ Respuesta incorrecta")
            self.toggle_page() 
            self.numRonda = 1


def index() -> rx.Component: #Pagina principal, en este caso muestra la uno o la dos según un booleano
    return rx.cond(State.show_page_one, page_one(), page_two())

def page_one(): #Pagina de inicio
    return rx.center(
        rx.vstack(
            rx.text("Bienvenido a QQSM", font_size="2em"),
            rx.button("Comenzar", on_click=[
                State.toggle_page,
                State.seleccionarPregunta
            ]
                
                )

        )
    )

def page_two():#Pagina con la pregunta y opciones
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

app = rx.App()
app.add_page(index)
