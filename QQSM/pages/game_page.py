import reflex as rx
from QQSM.states.game_state import GameState

def get_gradient_color(index):
    """
    Calcula un color en el gradiente de verde a rojo en función de la pregunta actual.
    """
    factor = index / 14  # Normaliza entre 0 y 1
    r = int(0 + factor * (255 - 0))  # De 0 a 255
    g = int(255 - factor * (255 - 0))  # De 255 a 0
    b = 0
    return f"rgb({r},{g},{b})"

def render_public_chart():
    letras = ["A", "B", "C", "D"]
    return rx.hstack(
        rx.foreach(
            GameState.public_stats,
            lambda porcentaje: rx.vstack(
                rx.text(f"{porcentaje}%", font_size="14px", color="white"),
                rx.box(
                    width="30px",
                    height=f"{porcentaje * 2}px",
                    background_color="#FFD700",
                    border_radius="5px"
                )
            )
        ),
        spacing="2",
        align="end",
        justify="start",
        margin_top="5",
        margin_left="0px",
        padding= "0"
    )

def render_call_box():
    return rx.box(
        rx.text(GameState.call_text, font_size="16px", color="white", white_space="pre-wrap"),
        width="300px",
        height="150px",
        overflow_y="auto",
        padding="10px",
        background_color="#333C57",
        border_radius="10px",
        border="2px solid #FFD700",
        box_shadow="0px 0px 10px rgba(255, 215, 0, 0.5)",
    )


@rx.page(route="/game")
def game_page():
    return rx.center(
        rx.box(
                rx.text("¿QUIÉN QUIERE SER MILLONARIO?",class_name="title-style"),
                    rx.center(
                        rx.vstack(
                            rx.hstack(
                                rx.button("✖", on_click=rx.redirect("/menu"), class_name="menu-exit-button"),
                                rx.spacer(),
                                *[   
                                    rx.box(
                                        rx.text(str(i + 1), font_size="14", color="gold", text_align="center"),  # Número en dorado
                                        rx.box(
                                            class_name=rx.cond(
                                                i == GameState.number_question - 1,  # Ajustado a 1-based index
                                                "progress-circle current",  # Pregunta actual resaltada
                                                "progress-circle"
                                            ),
                                            background_color=rx.cond(
                                                i < GameState.number_question,
                                                get_gradient_color(i),  # Color correspondiente
                                                "gray"  # Preguntas no alcanzadas
                                            )
                                        ),
                                        display="flex",
                                        flex_direction="column",
                                        align_items="center",
                                    )
                                    for i in range(15)
                                ],
                                rx.spacer(),
                                rx.cond(
                                    GameState.correct_answer,
                                    rx.button(
                                        "➜",  # Flecha Unicode
                                        on_click=GameState.next_round, 
                                        class_name="next-arrow-button"
                                    )
                                ),    
                                class_name="progress-container",
                                width="100%",
                            ),


                            rx.hstack(
                                rx.box(
                                    rx.text(GameState.question, font_size="24", font_weight="bold", color="white", text_align="center", class_name="custom-title"),
                                    padding="5",
                                    border_radius="5",
                                    width="80%",
                                    text_align="center",
                                ),
                                rx.box(
                                    rx.text(GameState.topic, class_name="custom-category"),
                                    width="100px",
                                    height="100px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                ),
                                spacing="5",
                                align="center",
                                justify="center",
                                margin_top="0px"
                            ),

                            spacing="5",
                            align="center"
                        ),
                ),

            rx.center(
                rx.vstack(
                    rx.hstack(
                        rx.cond(GameState.public_used, render_public_chart()),
                        rx.grid(
                            rx.button(f"A) {GameState.option_a}", width="100%", class_name=GameState.button_classes["A"], on_click=lambda: GameState.validate_answer("A"), disabled=GameState.chosen_answer),  
                            rx.button(f"B) {GameState.option_b}", width="100%", class_name=GameState.button_classes["B"], on_click=lambda: GameState.validate_answer("B"), disabled=GameState.chosen_answer),  
                            rx.button(f"C) {GameState.option_c}", width="100%", class_name=GameState.button_classes["C"], on_click=lambda: GameState.validate_answer("C"), disabled=GameState.chosen_answer),  
                            rx.button(f"D) {GameState.option_d}", width="100%", class_name=GameState.button_classes["D"], on_click=lambda: GameState.validate_answer("D"), disabled=GameState.chosen_answer),  
                            columns="2",
                            spacing="5",
                            align_items="center",
                            justify_content="center",
                            width="400px",
                        ),
                        rx.cond(GameState.call_used, render_call_box()),
                        spacing="5",
                        align="start",
                        justify="center"
                    ),
                ),
            ),

            rx.center(
                rx.text(GameState.feedback, font_size="20", color="red", margin_top="10px",text_align="center"),  # Mensaje de validación

                rx.hstack(
                    rx.button("📊", class_name="joker-button", on_click=GameState.use_public_option, disabled=GameState.public_used | GameState.chosen_answer),
                    rx.button("50%", class_name="joker-button", on_click=GameState.use_fifty_option, disabled=GameState.fifty_used | GameState.chosen_answer),
                    rx.button("📞", class_name="joker-button", on_click=GameState.use_call_option, disabled=GameState.call_used | GameState.chosen_answer),
                    spacing="7",
                    margin_top="15px"
                )                            
            ),
            width="100vw", height="100vh", background_color="#1E3A5F", min_height="100vh",overflow_y="auto"
        )
    )