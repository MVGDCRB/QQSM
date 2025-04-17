import reflex as rx
from QQSM.states.login_state import LoginState
from QQSM.states.leaderboard_state import LeaderboardState
from QQSM.styles.colors import Colors

def user_page():
    # componente de perfil (solo se verá si hay sesión)
    perfil = rx.center(
        rx.box(
            rx.vstack(
                rx.text("👤 PERFIL DE USUARIO", font_size="2em", color=Colors.GOLD),
                rx.text(f"Nombre de usuario: {LoginState.username}",
                        font_size="1.2em", color="white"),
                rx.text(f"Puntuación máxima: {LeaderboardState.max_score}",
                        font_size="1.2em", color="white"),
                rx.button("Volver al menú",
                          on_click=lambda: rx.redirect("/menu"),
                          class_name="custom-button",
                          margin_top="30px"),
                spacing="4",
                align="start",
            ),
            padding="40px",
            background_color=Colors.DARK_BLUE,
            border_radius="12px",
            width="400px",
        ),
        width="100vw",
        height="100vh",
        background_color=Colors.DARK_BLUE,
    )

    # componente vacío para la rama sin sesión
    vacio = rx.fragment()

    return rx.cond(LoginState.is_authenticated, perfil, vacio)
