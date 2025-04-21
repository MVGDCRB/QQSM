import reflex as rx
from QQSM.auth import get_top_10_users
from QQSM.states.login_state import LoginState
from QQSM.states.leaderboard_state import LeaderboardState
from QQSM.styles.colors import Colors


@rx.page(route="/leaderboard",on_load=LeaderboardState.load())
def leaderboard_page():
    # Top‑10 general
    top_users = get_top_10_users()

    # Fila permanente del visitante / usuario
    user_row = render_row(
        rx.cond(LoginState.is_authenticated, LeaderboardState.position, -1),
        rx.cond(LoginState.is_authenticated, LoginState.username, "No registrado"),
        rx.cond(LoginState.is_authenticated, LeaderboardState.max_score, -1),
        highlight=True,
    )

    # Fila resaltada dentro del Top‑10 si coincide con el usuario logueado
    top_rows = [
        render_row(
            i + 1,
            username,
            score,
            highlight=(
                LoginState.is_authenticated
                & (LoginState.username == username)
            ),
        )
        for i, (username, score) in enumerate(top_users)
    ]

    return rx.center(
        rx.box(
            rx.vstack(
                rx.text("🏆 LEADERBOARD", font_size="2em", color=Colors.GOLD),

                rx.box(
                    rx.vstack(*top_rows, spacing="0", align="stretch"),
                    max_height="400px",
                    overflow_y="auto",
                    width="100%",
                ),

                user_row,
                spacing="4",
            ),
            width="400px",
            padding="40px",
            background_color=Colors.DARK_BLUE,
            border_radius="12px",
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


def render_row(pos, username, score, highlight=False):
    """Renderiza una fila del ranking."""
    return rx.hstack(
        rx.text(f"{pos}.", width="25px", font_size="0.85em", color=Colors.GOLD),
        rx.text(username, font_size="0.85em", color="white",
                flex="1", text_align="left"),
        rx.box(
            rx.text(f"{score}", font_weight="bold",
                    color=Colors.GOLD, font_size="0.85em"),
            padding="1px 8px",
            background_color="#2D3748",
            border_radius="6px",
            border=f"1px solid {Colors.GOLD}",
            min_width="50px",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        width="100%",
        padding="4px 8px",
        background_color=rx.cond(highlight, "#2B3D5F", "#22314a"),
        border_radius="6px",
    )
