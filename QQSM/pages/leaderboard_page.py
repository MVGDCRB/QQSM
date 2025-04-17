import reflex as rx
from QQSM.auth import get_top_10_users           # ➊  leer directamente la BD
from QQSM.states.login_state import LoginState
from QQSM.styles.colors import Colors

def leaderboard_page():
    top_users = get_top_10_users()               # ➋  lista [(username, score)]

    # fila del usuario solo si hay login
    user_row = rx.cond(
        LoginState.is_authenticated,
        render_row(                             # ➌  usa los datos del login
            "—",                                # posición desconocida
            LoginState.username,
            rx.cond(LoginState.is_authenticated, 0, 0),   # score real se cargará aparte
            highlight=True,
        ),
        rx.fragment(),                          # ➍  nada si no hay usuario
    )

    return rx.center(
                    rx.box(
                        rx.vstack(
                            rx.text("🏆 LEADERBOARD", font_size="2em", color=Colors.GOLD),

                            # Top‑10 sin rx.foreach → no hay Var en la iteración
                            rx.box(
                                rx.vstack(
                                    *[
                                        render_row(i + 1, username, score)
                                        for i, (username, score) in enumerate(top_users)
                                    ],
                                    spacing="0",
                                    align="stretch",
                                ),
                                max_height="400px",
                                overflow_y="auto",
                                width="100%",
                            ),

                            # … resto de la página
                        ),
                        width="400px",
                        padding="40px",
                        background_color=Colors.DARK_BLUE,
                        border_radius="12px",
                        position="relative",
                    ),
                    width="100vw",
                    height="100vh",
                    background_color=Colors.DARK_BLUE,
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
