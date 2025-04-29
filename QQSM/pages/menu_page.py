import reflex as rx
from QQSM.states.game_state import GameState
from QQSM.styles.colors import Colors


@rx.page("/menu")
def menu_page():
    return rx.box(
        # Botón de salida fijo en la esquina superior izquierda
        rx.box(
            rx.button("✖", on_click=rx.redirect("/welcome"), class_name="menu-exit-button"),
            position="absolute",
            top="20px",
            left="20px",
            z_index="10"
        ),
        # Contenedor centrado vertical y horizontal con fondo liso y scroll interno
        rx.center(
            rx.box(
                rx.vstack(
                    rx.button("Modo Normal", on_click=GameState.initialize_game("/game"),
                              class_name="hex-button", width="300px"),
                    rx.button("Modo Infinito", on_click=GameState.initialize_game("/endless"),
                              class_name="hex-button", width="300px"),
                    rx.button("Modo Temas", on_click=GameState.initialize_game("/theme"),
                              class_name="hex-button", width="300px"),
                    rx.button("IA vs IA", on_click=rx.redirect("/maquinaVS"),
                              class_name="hex-button", width="300px"),
                    rx.button("Marcadores", on_click=rx.redirect("/leaderboard"),
                              class_name="hex-button", width="300px"),
                    rx.button("Perfil Usuario", on_click=rx.redirect("/user"),
                              class_name="hex-button", width="300px"),
                    spacing="8",
                    align="center",
                    min_height="0",
                ),
                background_color=Colors.DARK_BLUE,
                padding="30px",
                border_radius="10px",
                height="90vh",  # 5% arriba, 5% abajo
                overflow_y="auto",
                width="fit-content",
                margin_left="auto",
                margin_right="auto"
            ),
            height="100vh",
            width="100vw",
        ),
        width="100vw",
        height="100vh",
        background_image="url('/welcome_fondo.jpg')",
        background_size="cover",
        background_position="center",
        background_repeat="no-repeat",
        position="relative",
        overflow="hidden"
    )
