from QQSM.pages.components import *

DIFFICULTY_LEVELS: int = 15
TITLE: str = "¿QUIÉN QUIERE SER MILLONARIO?"

#Esquema general de la página con upper, lower, right, left y central panel

@rx.page(route="/game")
def game_page():
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

        rx.box(render_left_panel(), position="absolute", left="0px", bottom="15px"),
        rx.box(render_right_panel(), position="absolute", right="50px", bottom="50px"),

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
        render_next_button(GameState.correct_answer),
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

#Panel con la caja de texto con la respuesta de la IA a la llamada, si se muestra
def render_left_panel():
    return rx.box(
        rx.cond(
            GameState.call_used & (GameState.call_text != ""),
            render_call_box()
        ),
        width="25vw",
        height="55vh",
        background_color="transparent",
    )

#Panel con el gráfico de barras con las respuestas del público, si se muestran
def render_right_panel():
    return rx.box(
        rx.cond(
            GameState.public_used & (GameState.public_items != []),
            render_public_chart()
        ),
        width="25vw",
        height="33vh",
        background_color="transparent",
    )

# Panel inferior con los tres botones de comodín
def render_lower_panel():
    return rx.center(
        rx.hstack(
            render_joker_call(),
            render_joker_fifty(),
            render_joker_public(),
            spacing="6",
            margin_top="30px"
        ),
        width="100%"
    )
