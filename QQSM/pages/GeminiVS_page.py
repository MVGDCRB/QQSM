from QQSM.pages.components import *

DIFFICULTY_LEVELS: int = 15
TITLE: str = "¿QUIÉN QUIERE SER MILLONARIO?"

#Esquema general de la página con upper, lower y central panel

@rx.page(route="/GeminiVS")
def deep_seekia_page():
    return rx.box(
        render_upper_panel(),
        render_progress_indicator(DIFFICULTY_LEVELS),

        rx.hstack(
            render_central_panel(),
            spacing="6",
            align="start",
            justify="center"
        ),

        render_lower_panel(),
        render_feedback_line(),

        width="100vw",
        min_height="100vh",
        background_color=Colors.DARK_BLUE,
        spacing="4",
        align="center",
        position="relative",
        overflow="hidden",
    )

#Panel superior con botón de salida, título y botón de siguiente
def render_upper_panel():
    return rx.hstack(
        render_exit_button(),
        render_game_header(TITLE),
        render_next_button(True),
        width="100%",
        padding="0px 20px",
        align="center",
        justify="between",
    )

#Panel central con el enunciado y tema de la pregunta, así como las 4 posibles respuestas
def render_central_panel():
    return rx.vstack(
        rx.hstack(
            render_question_title(GameState.question),
            render_question_topic(GameState.topic),
            spacing="5",
            align="center",
            justify="center",
            width="100%"
        ),
        render_answer_options(),
        spacing="4",
        align="center",
        justify="center",
        width="66%",
        background_color=Colors.DARK_BLUE
    )

#No hay paneles izquierdo ni derecho porque no hay comodines en el modo IA vs

#Panel inferior, con los iconos de las IAs que están compitiendo y el texto VS costumizado entre ellas.Actualmente la primera siempres es Gemini.
def render_lower_panel():
    return rx.center(
        rx.hstack(
            render_ia_icon("gemini"),
            render_vs_text(),
            render_ia_icon(GameState.rival),
            spacing="6",
            margin_top="10px"
        ),
        width="100%"
    )
