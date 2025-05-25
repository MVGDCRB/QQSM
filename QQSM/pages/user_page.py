import reflex as rx
from QQSM.states.user_state import UserState
from QQSM.styles.colors import Colors
from QQSM.pages.components import render_exit_button

#Página reflex que genera la interfaz del perfil de usuario

@rx.page("/user", on_load=UserState.load_user_data())
def user_page():
    return rx.box(
        rx.vstack(
            rx.box(
                render_exit_button("/menu"),
                position="absolute",
                top="20px",
                left="20px"
            ),
            render_profile_data(),
            render_profile_stats(),
        ),
        width="100vw",
        min_height="100vh",
        background_image="url('/welcome_fondo.jpg')",
        background_size="cover",
        background_position="top center",
        background_attachment="fixed",
        background_repeat="no-repeat",
        position="relative",
        overflow_y="auto"
    )


#Componente que muestra los datos de perfil: nombre, puntuación, ranking, y preguntas respondidas totales
def render_profile_data() -> rx.Component:
    return rx.vstack(
            rx.box(
                rx.text(
                    "TU PERFIL",
                    class_name="title-style",
                    text_align="center",
                    background_color=Colors.TRANSPARENT_BG,
                    padding="10px",
                    border_radius="8px"
                ),
                width="100%",
                margin_top="40px"
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("Nombre de usuario:", font_weight="bold", color=Colors.GOLD),
                        rx.text(UserState.username, color="white"),
                        spacing="2"
                    ),
                    rx.hstack(
                        rx.text("Puntuación máxima:", font_weight="bold", color=Colors.GOLD),
                        rx.text(UserState.max_score, color="white"),
                        spacing="2"
                    ),
                    rx.hstack(
                        rx.text("Posición en el ranking:", font_weight="bold", color=Colors.GOLD),
                        rx.text(UserState.position, color="white"),
                        spacing="2"
                    ),
                    rx.hstack(
                        rx.text("Preguntas respondidas totales:", font_weight="bold", color=Colors.GOLD),
                        rx.text(UserState.total_questions, color="white"),
                        spacing="2"
                    ),
                    spacing="3",
                    padding="20px",
                    border_radius="8px",
                    background_color=Colors.DARK_BLUE,
                ),
                width="fit-content",
                margin="0 auto"
            ),
            spacing="5",
            width="100%",
            padding="30px",
            align="center",
            justify="start"
    )

#Componente que muestra una cuadrícula con las estadísticas de aciertos por cada tema, resaltando en color según rando de aciertos
def render_profile_stats() -> rx.Component:
    return rx.vstack(
            rx.box(
                rx.text(
                    "Estadísticas por tema",
                    font_size="1.4em",
                    color=Colors.GOLD,
                    background_color=Colors.TRANSPARENT_BG,
                    padding="8px",
                    border_radius="8px"
                ),
                margin_top="20px",
                width="fit-content"
            ),
            rx.grid(
                rx.foreach(
                    UserState.tema_stats,
                    lambda s: rx.box(
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    s.split(';')[0].upper(),
                                    font_weight="bold",
                                    color=Colors.GOLD,
                                    font_size="0.9em",
                                    margin_bottom="5px"
                                ),
                                rx.box(
                                    background_image=f"url('/themes/{s.split(';')[0]}.png')",
                                    class_name="theme-icon image",
                                    width="100px",
                                    height="100px",
                                    margin_bottom="5px",
                                    border_radius="50%",
                                    background_size="cover",
                                    background_position="center",
                                    **{"data-theme": s.split(';')[0]}
                                ),
                                rx.text(
                                    f"Aciertos: {s.split(';')[1]}/{s.split(';')[6]}",
                                    font_weight="bold",
                                    color=Colors.GOLD,
                                    margin_top="10px"
                                ),
                                spacing="1",
                                align="center",
                                id="normal-content"
                            ),
                            rx.center(
                                rx.vstack(
                                    rx.text(
                                        s.split(';')[0].upper(),
                                        font_size="1.2em",
                                        font_weight="bold",
                                        color=Colors.GOLD
                                    ),
                                    rx.text(
                                        "Porcentaje de precisión",
                                        font_size="1.5em",
                                        font_weight="bold",
                                        color=Colors.GOLD
                                    ),
                                    rx.text(
                                        f"{s.split(';')[3]}%",
                                        font_size="3em",
                                        font_weight="bold",
                                        color=s.split(';')[5]
                                    ),
                                    spacing="2",
                                    align="center"
                                ),
                                display="none",
                                id="hover-content"
                            ),
                            width="100%",
                            height="100%",
                            position="relative"
                        ),
                        padding="15px",
                        background_color=Colors.DARK_BLUE,
                        border=f"4px solid {s.split(';')[5]}",
                        border_radius="8px",
                        transition="all 0.3s ease",
                        _hover={
                            "transform": "scale(1.05)",
                            "#normal-content": {"display": "none"},
                            "#hover-content": {"display": "flex"}
                        }
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
    )
