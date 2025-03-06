import reflex as rx
from QQSM.states.game_state import GameState

@rx.page(route="/game")
def game_page():
    return rx.center(
        rx.vstack(
            rx.text("🎮 Quién Quiere Ser Millonario", font_size="50", font_weight="bold"),

            # Mostrar la ronda actual
            rx.text(f"Pregunta {GameState.number_question}", font_size="22", font_weight="bold", color="orange"),

            # Mostrar el tema y la dificultad
            rx.text(f"Tema: {GameState.topic}", font_size="20", font_weight="bold", color="purple"),
            rx.text(f"Dificultad: {GameState.difficulty}/100", font_size="18", color="gray"),

            #rx.text(GameState.question, font_size="18", color="blue", margin_top="10px"),
            
            rx.text(GameState.question, class_name="custom-title"),

            # Botones con opciones A, B, C, D con validación
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
                    width="400px",  # Ajusta el ancho si es necesario
                ),
                justify="center",
                width="100%"
            ),

            rx.text(GameState.feedback, font_size="20", color="red", margin_top="10px"),  # Mensaje de validación

            rx.hstack(
                rx.button("🃏 Usar 50:50", on_click=GameState.use_fifty_option, disabled=GameState.fifty_used | GameState.chosen_answer),
                rx.button("📊 Usar Comodín del Público", on_click=GameState.use_public_option, disabled=GameState.public_used | GameState.chosen_answer),
                rx.button("📊 Usar Comodín de la llamada", on_click=GameState.use_call_option, disabled=GameState.call_used | GameState.chosen_answer),
                spacing="5"
            ),

            # Mostrar el resultado del comodín del público
            rx.cond(GameState.public_used, rx.text(GameState.public_stats, font_size="16", color="green")),
            # Mostrar el resultado del comodin de la llamada
            rx.cond(GameState.call_used, rx.text(GameState.call_text, font_size="16", color="orange", width="500px", text_align="center")),

            rx.cond(
                GameState.correct_answer,
                rx.button("Siguiente Pregunta", on_click=GameState.next_round, margin_top="15px")
            ),
            rx.button("Volver al menú", on_click=rx.redirect("/menu"), margin_top="10px"),
        )
    )
