import reflex as rx
from QQSM.states.game_state import GameState
from QQSM.styles.styles import*
from QQSM.pages.components import*

#Título del menú
TITLE: str = "¡JUEGA!"

#Página reflex que genera la interfaz del menú principal de modos de juego
@rx.page("/menu")
def menu_page() -> rx.Component:
    return rx.box(
        rx.center(
            rx.hstack(
                rx.box(
                    render_exit_button("/welcome"),
                    position="absolute",
                    left="5%",
                    height="5vh",
                    margin_top="5%",
                ),
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
                            ),
                            render_game_mode_button("Modo clásico", "/game"),
                            render_game_mode_button("Modo infinito", "/endless"),
                            render_game_mode_button("Modo elección", "/theme"),
                            render_return_button("IA vs IA", "/maquinaVS"),
                            spacing="0",
                            align="center",
                            margin_bottom="5%"
                        ),
                        background_color=Colors.DARK_BLUE,
                        margin_top="5%",
                        border_radius="10px",
                        border=f"2px solid {Colors.GOLD}",
                        width="33vw",
                        height="95vh",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        overflow="hidden",
                    ),
                    render_redirect_circular_button("RANKING", "podium", "/leaderboard"),
                    spacing="5",
                    align="center",
                    justify="center",
                    height="95vh",
                ),
            )
        ),
        width="100vw",
        height="100vh",
        background_image=qqsm_background,
        background_position="center",
        background_repeat="no-repeat",
        position="relative",
        overflow="hidden"
    )
