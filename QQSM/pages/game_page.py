import reflex as rx
from QQSM.states.state import State

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