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
            on_click=GameState.next_round.debounce(1000),
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
    number = GameState.number_question

    return rx.hstack(
        *[
            rx.box(
                #Numeros de pregunta
                rx.text(
                    ((number - 1) // steps) * steps + (i + 1),
                    font_size="14px",
                    color="gold",
                    text_align="center",
                ),
                #circulos
                rx.box(
                    class_name=rx.cond(
                        i == (number - 1) % steps,
                        "progress-circle current",
                        "progress-circle",
                    ),
                    background_color=rx.cond(
                        i <= (number - 1) % steps,
                        get_gradient_color(i, steps),
                        "gray",
                    ),
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
        margin_bottom="5px",
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
    # Obtiene el tema actual; por defecto "arte" para pruebas
    theme = GameState.topic
    return rx.box(
        # Aplica la clase CSS que define forma, borde y sombra
        class_name="theme-icon image",
        # Inyecta la imagen del tema de forma dinámica
        background_image=f"url('/themes/{theme}.png')",
        **{"data-theme": GameState.topic},
        # Estas props aseguran el tamaño adecuado
        width="100px",
        height="100px",
        flex_shrink="0",
    )



def render_topic_choser():
    theme1 = GameState.topic_selection1
    theme2 = GameState.topic_selection2

    def icon_button(theme):
        return rx.button(
            rx.box(
                class_name="theme-icon image",
                background_image=f"url('/themes/{theme}.png')",
                **{"data-theme": theme},
                width="100px",
                height="100px",
            ),
            on_click=GameState.set_theme(theme),
            disabled=GameState.enable_topic,
            style={"padding": "0", "border": "none", "background": "none"},
        )

    return rx.hstack(
        icon_button(theme1),
        icon_button(theme2),
        spacing="5",
        align="center",
        justify="center",
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
            GameState.public_items,
            lambda item, idx: rx.vstack(
                # Mostrar porcentaje encima
                rx.text(f"{item[1]}%", font_size="14px", color="white"),
                # Barra de audiencia
                rx.box(
                    width="30px",
                    height=f"{item[1] * 2}px",
                    background_color=Colors.GOLD,
                    border_radius="5px",
                ),
                # Letra de la opción debajo de la barra
                rx.text(item[0], font_size="14px", color="white"),
                align="center",
                spacing="2",
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
        rx.center(
            rx.cond(
                GameState.call_loading,
                rx.text(
                    "📞 Llamando...",
                    font_size="1.1em",
                    color=Colors.GOLD,
                    animation="pulse 1.5s infinite",
                    text_align="center"
                ),
                rx.text(
                    GameState.call_text,
                    font_size="1.1em",
                    color="white",
                    text_align="left",  # ← para mejor lectura con scrollbar
                    white_space="pre-wrap",
                    word_break="break-word",
                )
            )
        ),
        width="220px",
        height="450px",
        background_color="#111827",
        padding="20px",
        border_radius="30px",
        border=f"2px solid {Colors.GOLD}",
        box_shadow="0 0 20px rgba(255, 215, 0, 0.5)",
        overflow_y="auto",  # ← scroll si el texto es largo
        display="flex",
        align_items="center",
        justify_content="center",
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
