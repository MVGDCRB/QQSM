from QQSM.pages.components import *

DIFFICULTY_LEVELS: int = 15
TITLE: str = "¿QUIÉN QUIERE SER MILLONARIO?"

#Esquema general de la página con upper, lower y central panel

@rx.page(route="/deepSeekIA")
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
        render_next_button(),
        width="100%",
        padding="0px 20px",
        align="center",
        justify="between",
    )

#Panel central con el enunciado y tema de la pregunta, así como las 4 posibles respuestas
def render_central_panel():
    return rx.vstack(
        rx.hstack(
            render_question_title(),
            render_question_topic(),
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

#No hay paneles izquierdo ni derecho porque no hay comodines en el modo IA

#Panel inferior, con los iconos de las IAs que están compitiendo y el texto VS costumizado entre ellas
def render_lower_panel():
    return rx.center(
        rx.hstack(
            rx.box(
                class_name="theme-icon image",
                background_image="url('/ias/gemini.png')",
                **{"data-theme": "gemini"},
                width="100px",
                height="100px",
            ),
            rx.text(
                "VS",
                font_size="4em",
                font_weight="bold",
                font_family="Impact, sans-serif",
                color="transparent",
                background="linear-gradient(180deg, #FFD700, #FF4500, #8B0000)",
                background_clip="text",
                text_shadow=(
                    "1px 1px 1px black, "
                    "0 0 4px #FF4500, "
                    "0 0 8px #FF8C00"
                ),
                margin="0 20px",
                height="100px",
                line_height="100px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.box(
                class_name="theme-icon image",
                background_image="url('/ias/deepSeek.png')",
                **{"data-theme": "deepSeek"},
                width="100px",
                height="100px",
            ),
            spacing="6",
            margin_top="10px"
        ),
        width="100%"
    )
