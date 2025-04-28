import reflex as rx
from QQSM.styles.colors import Colors
from QQSM.states.game_state import GameState


@rx.page(route="/openAI")
def openaiia_page():
    return rx.box(
        render_upper_panel(),
        render_progress_indicator(),

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
        render_next_button(),
        width="100%",
        padding="0px 20px",
        align="center",
        justify="between",
    )


def render_game_header():
    return rx.box(
        rx.text(
            "¿QUIÉN QUIERE SER MILLONARIO? OpenAI vs Gemini",
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


def render_next_button():
    return rx.cond(
        GameState.correct_answer,
        rx.button(
            "➜",
            on_click=GameState.next_round,
            class_name="next-arrow-button"
        )
    )


def get_gradient_color(index):
    factor = index / 14
    r = int(0 + factor * 255)
    g = int(255 - factor * 255)
    b = 0
    return f"rgb({r},{g},{b})"


def render_progress_indicator():
    return rx.hstack(
        *[
            rx.box(
                rx.text(str(i + 1), font_size="14px", color="gold", text_align="center"),
                rx.box(
                    class_name=rx.cond(
                        i == GameState.number_question - 1,
                        "progress-circle current",
                        "progress-circle"
                    ),
                    background_color=rx.cond(
                        i < GameState.number_question,
                        get_gradient_color(i),
                        "gray"
                    )
                ),
                display="flex",
                flex_direction="column",
                align_items="center",
            )
            for i in range(15)
        ],
        spacing="6",
        align="center",
        justify="center",
        class_name="progress-container",
        width="100%",
        margin_bottom="5px"
    )


def render_question_section():
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


def render_question_title():
    return rx.box(
        rx.text(
            GameState.question,
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


def render_question_topic():
    return rx.box(
        rx.text(GameState.topic, class_name="custom-category"),
        width="100px",
        height="100px",
        display="flex",
        align_items="center",
        justify_content="center",
        border_radius="50%",
        background_color=Colors.GOLD,
        flex_shrink="0"
    )


def render_answer_options():
    return rx.grid(
        *[
            rx.button(
                f"{letter}) {getattr(GameState, f'option_{letter.lower()}')}",
                width="100%",
                font_size="14px",
                white_space="normal",
                word_break="break-word",
                height="auto",
                min_height="50px",
                class_name=GameState.button_classes[letter],
                on_click=lambda le=letter: GameState.validate_answer(le),
                disabled=GameState.chosen_answer
            )
            for letter in ["A", "B", "C", "D"]
        ],
        columns="2",
        spacing="4",
        width="70%",  
        align_items="center",
        justify_content="center",
        margin_top="10px",
    )
