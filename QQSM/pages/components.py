import reflex as rx
from QQSM.states.game_state import GameState
from QQSM.styles.colors import Colors
from reflex import Style

def render_exit_button():
    return rx.button(
        "✖",
        on_click=rx.redirect("/menu"),
        class_name="menu-exit-button"
    )


def render_game_header(text: str):
    return rx.box(
        rx.text(
            text,
            class_name="title-style",
            margin="0px"
        ),
        width="100%",
        padding="0px",
        text_align="center"
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

def get_gradient_color(index: int, steps: int) -> str:
    factor = index / (steps - 1) if steps > 1 else 0
    r = int(factor * 255)
    g = int((1 - factor) * 255)
    b = 0
    return f"rgb({r},{g},{b})"


def render_progress_indicator(steps: int):
    return rx.hstack(
        *[
            rx.box(
                rx.text(str(i + 1), font_size="14px", color="gold", text_align="center"),
                rx.box(
                    class_name=rx.cond(
                        i == (GameState.number_question - 1) % steps,
                        "progress-circle current",
                        "progress-circle"
                    ),
                    background_color=rx.cond(
                        i < GameState.number_question,
                        get_gradient_color(i, steps),
                        "gray"
                    )
                ),
                display="flex",
                flex_direction="column",
                align_items="center",
            )
            for i in range(steps)
        ],
        spacing="6",
        align="center",
        justify="center",
        class_name="progress-container",
        width="100%",
        margin_bottom="5px"
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

def render_topic_chooser():
    return rx.hstack(
        rx.button(
            f"{GameState.topic_selection1}",
            on_click=GameState.set_theme(GameState.topic_selection1),
            class_name="custom-category",
            width="100px",
            height="100px",
            display="flex",
            align_items="center",
            justify_content="center",
            disabled=GameState.enable_topic,
        ),
        rx.button(
            f"{GameState.topic_selection2}",
            on_click=GameState.set_theme(GameState.topic_selection2),
            class_name="custom-category",
            width="100px",
            height="100px",
            display="flex",
            align_items="center",
            justify_content="center",
            disabled=GameState.enable_topic,
        ),
        spacing="5",
        align="center",
        justify="center"
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

def render_public_chart():
    return rx.hstack(
        rx.foreach(
            GameState.public_stats,
            lambda porcentaje: rx.vstack(
                rx.text(f"{porcentaje}%", font_size="14px", color="white"),
                rx.box(
                    width="30px",
                    height=f"{porcentaje * 2}px",
                    background_color=Colors.GOLD,
                    border_radius="5px"
                )
            )
        ),
        width="25vw",
        height="33vh",
        spacing="3",
        align="end",
        justify="end",
    )


def render_call_box():
    return rx.box(
        rx.text(
            GameState.call_text,
            font_size="16px",
            color="white",
            white_space="pre-wrap",
            text_align="left"
        ),
        width="25vw",
        height="55vh",
        overflow_y="auto",
        padding="12px",
        background_color="#333C57",
        border_radius="10px",
        border="2px solid #FFD700",
        box_shadow="0px 0px 10px rgba(255, 215, 0, 0.5)",
        style=Style({"direction": "rtl"})
    )


def render_joker_call():
    return rx.button(
        "📞",
        class_name="joker-button",
        on_click=GameState.use_call_option,
        disabled=GameState.call_used | GameState.chosen_answer
    )

def render_joker_fifty():
    return rx.button(
        "50%",
        class_name="joker-button",
        on_click=GameState.use_fifty_option,
        disabled=GameState.fifty_used | GameState.chosen_answer
    )

def render_joker_public():
    return rx.button(
        "📊",
        class_name="joker-button",
        on_click=GameState.use_public_option,
        disabled=GameState.public_used | GameState.chosen_answer
    )


def render_feedback_line():
    return rx.cond(
        GameState.feedback != "",
        rx.box(
            rx.text(
                GameState.feedback,
                font_size="16px",
                color="white",
                text_align="center"
            ),
            width="100%",
            padding="10px",
            position="absolute",
            bottom="0px",
            text_align="center"
        )
    )