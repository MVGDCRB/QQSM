from QQSM.pages.components import *

#Número de niveles de dificultad
DIFFICULTY_LEVELS: int = 15

#Título de la página
TITLE: str = "¿QUIÉN QUIERE SER MILLONARIO?"

#Página reflex que genera la interfaz del modo de juego temático
@rx.page(route="/theme")
def theme_page() -> rx.Component:
    #Esquema general de la página con upper, lower, right, left y central panel
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
def render_upper_panel() -> rx.Component:
    return rx.hstack(
        render_exit_button("/menu"),
        render_header("¿QUIÉN QUIERE SER MILLONARIO?"),
        render_next_button(GameState.correct_answer),
        width="100%",
        padding="0px 20px",
        align="center",
        justify="between",
    )

#Panel central con el enunciado y tema de la pregunta, así como las 4 posibles respuestas
def render_central_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            render_question_title(GameState.question),
            render_topic_choser(GameState.topic_selection1, GameState.topic_selection2),
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

#Panel con el gráfico de barras con las respuestas del público, si se muestran
def render_right_panel() -> rx.Component:
    return rx.cond(
        GameState.public_used,
        render_public_chart()
    )

#Panel con la caja de texto con la respuesta de la IA a la llamada, si se muestra
def render_left_panel() -> rx.Component:
    return rx.cond(
        GameState.call_used,
        render_call_box()
    )

# Panel inferior con los tres botones de comodín
def render_lower_panel() -> rx.Component:
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
