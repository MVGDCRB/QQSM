import reflex as rx
from attr.validators import disabled
from keyring.core import disable
from QQSM.states.game_state import GameState
from QQSM.styles.colors import Colors
from QQSM.pages.components import *


@rx.page(route="/theme")
def theme_page():
    return rx.box(
        render_upper_panel(),
        # En función del número de circulitos
        render_progress_indicator(15),

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


def render_upper_panel():
    return rx.hstack(
        render_exit_button(),
        render_game_header("¿QUIÉN QUIERE SER MILLONARIO?"),
        render_next_button(),
        width="100%",
        padding="0px 20px",
        align="center",
        justify="between",
    )


def render_central_panel():
    return rx.vstack(
        rx.hstack(
            render_question_title(),
            render_topic_chooser(),
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


def render_right_panel():
    return rx.cond(
        GameState.public_used,
        render_public_chart()
    )


def render_left_panel():
    return rx.cond(
        GameState.call_used,
        render_call_box()
    )


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
