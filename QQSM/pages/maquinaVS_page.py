import reflex as rx
from QQSM.styles.colors import Colors
from QQSM.states.game_state import GameState

@rx.page(route="/maquinaVS_page")
def maquinaVS_page():
    return rx.box(
        render_upper_panel(),

        rx.hstack(
            render_question_section(),
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

def render_upper_panel():
    return rx.hstack(
        render_exit_button(),
        render_game_header(),
        width="100%",
        padding="0px 20px",
        align="center",
        justify="between",
    )

def render_game_header():
    return rx.box(
        rx.text(
            "¿QUIÉN QUIERE SER MILLONARIO? IA vs IA",
            class_name="title-style",
            margin="0px"
        ),
        width="100%",
        padding="0px",
        text_align="center"
    )


def render_exit_button():
    return rx.button(
        "✖",
        on_click=rx.redirect("/menu"),
        class_name="menu-exit-button"
    )


def get_gradient_color(index):
    factor = index / 14
    r = int(0 + factor * 255)
    g = int(255 - factor * 255)
    b = 0
    return f"rgb({r},{g},{b})"


def render_question_section():
    return rx.vstack(
        rx.hstack(
            render_text(),
            spacing="5",
            align="center",
            justify="center",
            width="100%"
        ),
        render_IAs(),
        spacing="4",
        align="center",
        justify="center",
        width="66%",
        background_color=Colors.DARK_BLUE
    )


def render_text():
    return rx.box(
        rx.text(
            "Elige la IA que vaya a responder la pregunta",
            white_space="normal",
            word_break="break-word",
            color="white",
            text_align="center",
            class_name="custom-title",
        ),
        width="70%",
        padding="5px",
        border_radius="8px",
    )


def render_IAs():
    return rx.hstack(
        render_IA1(),
        render_IA2(),
        render_IA3(),
         width="100px",
        height="100px",
        display="flex",
        align_items="center",
        justify_content="center",
        border_radius="50%",
        background_color=Colors.GOLD,
        flex_shrink="0"
    )

def render_IA1():
    return rx.box(
        rx.text("DeepSeek", class_name="custom-category", on_click=GameState.initialize_game("/deepSeekIA")),
    )

def render_IA2():
    return rx.box(
        rx.text("OpenAI", class_name="custom-category", on_click=GameState.initialize_game("/openAI")),
    )

def render_IA3():
    return rx.box(
        rx.text("LlamaIA", class_name="custom-category", on_click=GameState.initialize_game("/llamaAI")),
    )


