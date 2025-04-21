import reflex as rx
from QQSM.states.user_state import UserState
from QQSM.styles.colors import Colors

@rx.page("/user", on_load=UserState.load_user_data())
def user_page():
    return rx.center(
        rx.box(
            rx.vstack(
                rx.text("👤 PERFIL DE USUARIO", font_size="2em", color=Colors.GOLD),
                rx.text(f"Nombre de usuario: {UserState.username}", font_size="1.2em", color="white"),
                rx.text(f"Puntuación máxima: {UserState.max_score}", font_size="1.2em", color="white"),
                rx.text(f"Posición global: {UserState.position}", font_size="1.2em", color="white"),
                rx.box(
                    rx.text("Estadísticas por tema", font_size="1.2em", color=Colors.GOLD),
                    rx.grid(
                        rx.foreach(
                        UserState.tema_stats,
                        lambda s: rx.box(
                            rx.text(s.split(";")[0], font_weight="bold", color=Colors.GOLD, text_transform="capitalize"),
                            rx.text(f"Aciertos: {s.split(';')[1]} ({s.split(';')[3]}%)"),
                            rx.text(f"Fallos: {s.split(';')[2]} ({s.split(';')[4]}%)"),
                            padding="10px",
                            background_color="#2B3D5F",
                            border_radius="8px"
                            )
                        ),
                        columns="3",
                        spacing="4"
                    )
                ),
                spacing="4"
            ),
            padding="40px",
            background_color=Colors.DARK_BLUE,
            border_radius="12px",
            width="fit-content",
            position="relative",
        ),
        rx.box(
            rx.button("✖", on_click=rx.redirect("/menu"), class_name="menu-exit-button"),
            position="absolute",
            top="20px",
            left="20px",
        ),
        width="100vw",
        height="100vh",
        background_color=Colors.DARK_BLUE,
        position="relative",
    )
