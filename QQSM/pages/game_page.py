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
                                class_name="progress-container",
                                width="100%",
                            ),


                            rx.hstack(
                                rx.box(
                                    rx.text(GameState.question, font_size="24", font_weight="bold", color="white", text_align="center", class_name="custom-title"),
                                    padding="20px",
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
                    rx.flex(
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
                        justify="center",
                        width="100%"
                    ),
                ),
            ),

            rx.center(
                rx.text(GameState.feedback, font_size="20", color="red", margin_top="10px",text_align="center"),  # Mensaje de validación

                rx.hstack(
                    rx.button("50%", class_name="joker-button", on_click=GameState.use_fifty_option, disabled=GameState.fifty_used | GameState.chosen_answer),
                    rx.button("📊", class_name="joker-button", on_click=GameState.use_public_option, disabled=GameState.public_used | GameState.chosen_answer),
                    rx.button("📞", class_name="joker-button", on_click=GameState.use_call_option, disabled=GameState.call_used | GameState.chosen_answer),
                    spacing="7",
                    margin_top="15px"
                ),

                # Mostrar el resultado del comodín del público
                rx.cond(GameState.public_used, rx.text(GameState.public_stats, font_size="16", color="green")),
                # Mostrar el resultado del comodin de la llamada
                rx.cond(GameState.call_used, rx.text(GameState.call_text, font_size="16", color="orange", width="500px", text_align="center")),

                rx.cond(
                    GameState.correct_answer,
                    rx.button("Siguiente Pregunta", on_click=GameState.next_round, margin_top="15px")
                )      
            ),
            width="100vw", height="100vh", background_color="#1E3A5F", min_height="100vh",overflow_y="auto"
        )
    )