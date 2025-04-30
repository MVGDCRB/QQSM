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
        # Contenedor principal centrado con íconos laterales y menú en el centro
        rx.center(
            rx.hstack(
                # Ícono de perfil (izquierda)
                rx.button(
                    rx.box(
                        class_name="theme-icon image",
                        background_image="url('/buttons/user.png')",
                        **{"data-theme": "Tu perfil"},
                        width="100px",
                        height="100px",
                    ),
                    on_click=rx.redirect("/user"),
                    style={"padding": "0", "border": "none", "background": "none"},
                ),

                # Menú central con título y botones
                rx.box(
                    rx.vstack(
                        rx.box(
                            rx.text(
                                "¡JUEGA!",
                                color=Colors.ORANGE_BORDER,
                                font_size="1.5em",
                                font_weight="bold",
                                text_transform="uppercase",
                                text_align="center",
                                letter_spacing="1px",
                                width="100%",
                            ),
                            height="10%",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            width="100%",
                            margin_bottom="10%",
                        ),
                        rx.button(
                            "Modo clásico",
                            on_click=GameState.initialize_game("/game"),
                            class_name="hex-button",
                            width="300px",
                            margin_bottom="10%",
                        ),
                        rx.button(
                            "Modo Infinito",
                            on_click=GameState.initialize_game("/endless"),
                            class_name="hex-button",
                            width="300px",
                            margin_bottom="10%",
                        ),
                        rx.button(
                            "Modo Elección", #modo temas?
                            on_click=GameState.initialize_game("/theme"),
                            class_name="hex-button",
                            width="300px",
                            margin_bottom="10%",
                        ),
                        rx.button(
                            "IA vs IA",
                            on_click=rx.redirect("/maquinaVS"),
                            class_name="hex-button",
                            width="300px"
                        ),
                        spacing="0",  # espaciado eliminado, usamos margin_bottom
                        align="center",
                        min_height="0",
                    ),
                    background_color=Colors.DARK_BLUE,
                    border_radius="10px",
                    border=f"2px solid {Colors.GOLD}",
                    padding="30px",
                    height="90vh",
                    overflow_y="hidden",
                    width="fit-content",
                ),

                # Ícono de ranking (derecha)
                rx.button(
                    rx.box(
                        class_name="theme-icon image",
                        background_image="url('/buttons/podium.png')",
                        **{"data-theme": "ranking"},
                        width="100px",
                        height="100px",
                    ),
                    on_click=rx.redirect("/leaderboard"),
                    style={"padding": "0", "border": "none", "background": "none"},
                ),

                spacing="5",
                align="center",
                justify="center",
                height="100vh",
            )
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
