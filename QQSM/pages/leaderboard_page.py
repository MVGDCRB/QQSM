import reflex as rx
from QQSM.auth import get_top_10_users, get_user_leaderboard, get_user_position
from QQSM.styles.colors import Colors
from QQSM.states.login_state import LoginState


def leaderboard_page():
    current_user = LoginState.username
    top_users = get_top_10_users()
    user_data = get_user_leaderboard(current_user)
    current_user_score = user_data[0][1] if user_data else 0
    position = get_user_position(current_user)

    return rx.center(
        rx.box(
            rx.vstack(
                rx.text("🏆 LEADERBOARD", font_size="2em", color=Colors.GOLD),

                # Podium con scroll
                rx.box(
                    rx.vstack(
                        *[render_row(i + 1, username, score) for i, (username, score) in enumerate(top_users)],
                        spacing="0",
                        align="stretch",
                    ),
                    max_height="400px",
                    overflow_y="auto",
                    width="100%",
                ),

                # Línea del usuario actual
                rx.box(
                    render_row(position, current_user, current_user_score, highlight=True),
                    width="100%",
                    margin_top="20px"
                ),

                spacing="4",
                align="center",
            ),
            width="400px",
            padding="40px",
            background_color=Colors.DARK_BLUE,
            border_radius="12px",
            position="relative"
        ),

        # Botón cerrar arriba izquierda
        rx.box(
            rx.button("✖", on_click=rx.redirect("/menu"), class_name="menu-exit-button"),
            position="absolute",
            top="20px",
            left="20px"
        ),

        width="100vw",
        height="100vh",
        background_color=Colors.DARK_BLUE,
        overflow="hidden",
        position="relative"
    )


def render_row(pos, username: str, score: int, highlight: bool = False):
    return rx.hstack(
        rx.text(f"{pos}.", width="25px", font_size="0.85em", color=Colors.GOLD),
        rx.text(username, font_size="0.85em", color="white", flex="1", text_align="left"),
        rx.box(
            rx.text(f"{score}", font_weight="bold", color=Colors.GOLD, font_size="0.85em"),
            padding="1px 8px",
            background_color="#2D3748",
            border_radius="6px",
            border=f"1px solid {Colors.GOLD}",
            min_width="50px",
            display="flex",
            align_items="center",
            justify_content="center"
        ),
        width="100%",
        padding="4px 8px",
        background_color="#22314a" if not highlight else "#2B3D5F",
        border_radius="6px"
    )
