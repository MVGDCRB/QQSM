import reflex as rx
from QQSM.states.login_state import LoginState
from QQSM.states.leaderboard_state import LeaderboardState
from QQSM.styles.colors import Colors


@rx.page("/user_page")
def user_page():
    return rx.center(
        rx.box(
            rx.vstack(
                rx.text("👤 PERFIL DE USUARIO", font_size="2em", color=Colors.GOLD),
                rx.text(
                    rx.cond(
                        LoginState.is_authenticated,
                        f"Nombre de usuario: {LoginState.username}",
                        "Nombre de usuario: No registrado",
                    ),
                    font_size="1.2em",
                    color="white",
                ),

                rx.text(
                    rx.cond(
                        LoginState.is_authenticated,
                        f"Puntuación máxima: {LeaderboardState.max_score}",
                        "Puntuación máxima: -1",
                    ),
                    font_size="1.2em",
                    color="white",
                ),  
            ),
            padding="40px",
            background_color=Colors.DARK_BLUE,
            border_radius="12px",
            width="400px",
            position="relative",
        ),

        rx.box(
            rx.button("✖",
                      on_click=rx.redirect("/menu"),
                      class_name="menu-exit-button"),
            position="absolute",
            top="20px",
            left="20px",
        ),

        width="100vw",
        height="100vh",
        background_color=Colors.DARK_BLUE,
        position="relative",
    )
