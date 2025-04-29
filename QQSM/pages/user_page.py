import reflex as rx
from QQSM.states.user_state import UserState
from QQSM.styles.colors import Colors
from QQSM.pages.components import render_exit_button

@rx.page("/user", on_load=UserState.load_user_data())
def user_page():
    return rx.box(
        rx.vstack(
            rx.hstack(
                render_exit_button(),
                rx.text("PERFIL DE USUARIO", class_name="title-style"),
                justify="between",
                width="100%",
                padding="10px 20px"
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("Usuario:", font_weight="bold", color=Colors.GOLD),
                        rx.text(UserState.username, color="white"),
                        spacing="2"
                    ),
                    rx.hstack(
                        rx.text("Puntuación máxima:", font_weight="bold", color=Colors.GOLD),
                        rx.text(UserState.max_score, color="white"),
                        spacing="2"
                    ),
                    rx.hstack(
                        rx.text("Posición global:", font_weight="bold", color=Colors.GOLD),
                        rx.text(UserState.position, color="white"),
                        spacing="2"
                    ),
                    spacing="3",
                    padding="20px",
                    border_radius="8px",
                    background_color="#2B3D5F"
                ),
                width="fit-content",
                margin="0 auto"
            ),
            rx.text("Estadísticas por tema", font_size="1.4em", color=Colors.GOLD, margin_top="20px"),
            rx.grid(
                rx.foreach(
                    UserState.tema_stats,
                    lambda s: rx.box(
                        rx.vstack(
                            rx.image(src=f"/themes/{s.split(';')[0]}.png", width="50px", height="50px"),
                            rx.text(s.split(";")[0], font_weight="bold", color=Colors.GOLD),
                            rx.hstack(
                                rx.text("Aciertos:", font_weight="bold"),
                                rx.text(f"{s.split(';')[1]} ({s.split(';')[3]}%)")
                            ),
                            rx.hstack(
                                rx.text("Fallos:", font_weight="bold"),
                                rx.text(f"{s.split(';')[2]} ({s.split(';')[4]}%)")
                            ),
                            spacing="1",
                            align="center"
                        ),
                        padding="15px",
                        background_color="#1F2A44",
                        border_radius="8px",
                        box_shadow="0 0 10px rgba(255, 215, 0, 0.2)"
                    )
                ),
                columns="3",
                spacing="4",
                width="100%",
                justify_content="center",
                margin_top="10px"
            ),
            spacing="5",
            width="100%",
            padding="30px",
            align="center",
            justify="start"
        ),
        width="100vw",
        min_height="100vh",
        background_image="url('/welcome_fondo.jpg')",
        background_size="cover",
        background_position="center",
        background_repeat="no-repeat",
        position="relative",
        overflow_y="auto"
    )
