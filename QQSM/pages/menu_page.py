import reflex as rx
from QQSM.states.game_state import GameState
from QQSM.styles.colors import Colors
from QQSM.pages.components import*

#Título del menú
TITLE: str = "¡JUEGA!"

#Página reflex que genera la interfaz del menú principal de modos de juego
@rx.page("/menu")
def menu_page():
    return rx.box(
        render_exit_button("/welcome"),
        rx.center(
            rx.hstack(
                render_redirect_circular_button("TU PERFIL", "user", "/user"),
                rx.box(
                    rx.vstack(
                        rx.box(
                            render_subheader(TITLE),
                            height="10%",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            width="100%",
                            margin_bottom="10%",
                        ),
                        render_game_mode_button("Modo clásico", "/game"),
                        render_game_mode_button("Modo infinito", "/endless"),
                        render_game_mode_button("Modo elección", "/theme"),
                        render_return_button("IA vs IA", "/maquinaVS"),
                        spacing="0",
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
                render_redirect_circular_button("RANKING", "podium", "/leaderboard"),
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
