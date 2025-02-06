import reflex as rx
from rxconfig import config
from QQSM.auth import create_user, login_user
import random
from QQSM.db import init_db, SessionLocal


# Inicializa la base de datos y crea las tablas antes de ejecutar Reflex
init_db()

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
    numRonda: int = 1

    # Variables de usuario
    username: str = ""
    password: str = ""
    is_authenticated: bool = False

    def set_username(self, username: str):
        """Método para actualizar el estado de username"""
        self.username = username

    def set_password(self, password: str):
        """Método para actualizar el estado de la contraseña"""
        self.password = password

    def toggle_page(self):
        self.show_page_one = not self.show_page_one

    def seleccionarPregunta(self):
        self.textoPregunta, self.textoOpciones, self.opcionCorrecta = self.quiz_questions[self.numRonda - 1]

    def verificar_respuesta(self, seleccion: int):
        if seleccion == self.opcionCorrecta:
            print("✅ Respuesta correcta")
            self.numRonda += 1

            if self.numRonda == self.totalPreguntas:
                self.numRonda = 1
                self.toggle_page()
            else:
                self.seleccionarPregunta()
        else:
            print("❌ Respuesta incorrecta")
            self.toggle_page()
            self.numRonda = 1


    def handle_register(self):
        """Función de registro del usuario"""
        db = SessionLocal() #guardo la sesionLocal en una variable
        try:
            create_user(self.username, self.password, db)  # se pasa db junto al usuario y contraseña hasheada
            print("✅ Usuario registrado con éxito")
        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")
        finally:
            db.close()

    def handle_login(self):
        """Función de inicio de sesión del usuario"""
        if login_user(self.username, self.password):
            print("✅ Login exitoso")
            self.is_authenticated = True
        else:
            print("❌ Error de autenticación")


def index() -> rx.Component:
    return rx.cond(State.is_authenticated, game_page(), login_page()) #si esta registrado te manda al index sino al login


def login_page(): #TODO cambiar el login en login y registro por separado
    return rx.center(
        rx.vstack(
            rx.text("Iniciar sesión o registrarse", font_size="2em"),
            rx.input(placeholder="Usuario", on_blur=lambda: State.set_username(State.username)),  
            rx.input(placeholder="Contraseña", type="password", on_blur=lambda: State.set_password(State.password)),
            rx.button("Iniciar sesión", on_click=State.handle_login),
            rx.button("Registrar usuario", on_click=State.handle_register),
        )
    )


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


app = rx.App()
app.add_page(index)
