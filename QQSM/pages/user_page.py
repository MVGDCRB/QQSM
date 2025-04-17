import reflex as rx
from QQSM.auth import get_user_leaderboard
from QQSM.states.login_state import LoginState
from QQSM.styles.colors import Colors

@rx.page(route="/user_page")
def user_page():
    user_data = get_user_leaderboard(LoginState.username)
    username = LoginState.username
    max_score = user_data[0][1] if user_data else 0

    return rx.center(
        rx.box(
            rx.vstack(
                rx.text("👤 PERFIL DE USUARIO", font_size="2em", color=Colors.GOLD),

                rx.text(f"Nombre de usuario: {username}", font_size="1.2em", color="white"),
                rx.text(f"Puntuación máxima: {max_score}", font_size="1.2em", color="white"),

                rx.button("Volver al menú", on_click=rx.redirect("/menu"), class_name="hex-button", margin_top="30px"),

                spacing="4",
                align="start",
            ),
            padding="40px",
            background_color=Colors.DARK_BLUE,
            border_radius="12px",
            box_shadow="0px 0px 15px rgba(255, 255, 255, 0.1)",
            width="400px"
        ),
        width="100vw",
        height="100vh",
        background_color=Colors.DARK_BLUE
    )
