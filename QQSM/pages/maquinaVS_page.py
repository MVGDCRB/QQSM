import reflex as rx
from QQSM.styles.colors import Colors
from QQSM.states.game_state import GameState
from QQSM.pages.components import *

#Título de la página
TITLE: str = "¿QUIÉN QUIERE SER MILLONARIO? IA vs IA"

#Texto del selectori de IA rival
IA_SELECTION_TEXT = "Elige la IA que vaya a responder la pregunta"

#Página reflex que genera la interfaz del selector de IA rival en el modo máquina VS máquina
@rx.page(route="/maquinaVS")
def maquina_vs_page():
    #Esquema general de la página con upper y central panel
    return rx.box(
        render_upper_panel(),

        rx.hstack(
            render_central_panel(),
            spacing="6",
            align="start",
            justify="center"
        ),

        width="100vw",
        min_height="100vh",
        background_color=Colors.DARK_BLUE,
        spacing="4",
        align="center",
        position="relative",
        overflow="hidden",
    )

#Panel superior con botón de salida y título
def render_upper_panel():
    return rx.hstack(
        render_exit_button("/menu"),
        render_header(TITLE),
        width="100%",
        padding="0px 20px",
        align="center",
        justify="between",
    )

#Panel central con texto de selección de IAs con los iconos selectores correspondientes de cada IA
def render_central_panel() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                render_question_title(IA_SELECTION_TEXT),
                align="center",
                justify="center",
                width="100%"
            ),
            render_ia_chooser(),
            spacing="8",
            align="center",
            justify="center",
            width="66%",
        ),
        height="80vh",
        align_items="center",
        justify_content="center",
        width="100%",
        background_color=Colors.DARK_BLUE
    )

