import reflex as rx
from QQSM.states.login_state import LoginState
from QQSM.states.leaderboard_state import LeaderboardState
from QQSM.styles.colors import Colors
from QQSM.pages.components import render_exit_button

#Datos del usuario loggeado
user_row: rx.Component = None

#Datos de los 10 usuarios con mayor puntuacion
top_rows: rx.Component = None

@rx.page(route="/leaderboard", on_load=LeaderboardState.load())
def leaderboard_page():

    global user_row, top_rows
    # Se inicializan los datos del usuario
    user_row = render_row(
        rx.cond(LoginState.is_authenticated, LeaderboardState.position, -1),
        rx.cond(LoginState.is_authenticated, LoginState.username, "No registrado"),
        rx.cond(LoginState.is_authenticated, LeaderboardState.max_score, -1),
        highlight=True,
    )

    #Se inicializa el top 10
    top_rows = rx.foreach(
        LeaderboardState.top_users,
        lambda t: render_row(
            t[0],          # posición
            t[1],          # username
            t[2],          # score
            highlight=(
                LoginState.is_authenticated & (LoginState.username == t[1])
            )
        )
    )

    return rx.center(
        render_ranking(),
        rx.box(
            render_exit_button(),
            position="absolute",
            top="20px",
            left="20px",
        ),
        width="100vw",
        height="100vh",
        overflow="hidden",
        background_image="url('/welcome_fondo.jpg')",
        background_size="cover",
        background_position="center",
        background_repeat="no-repeat",
        position="relative",
    )

# Tabla del top 10
def render_ranking()-> rx.Component:
        return rx.box(
            rx.vstack(
                rx.text("🏆 LEADERBOARD", font_size="2em", color=Colors.GOLD),

                rx.box(
                    rx.vstack(top_rows, spacing="0", align="stretch"),
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
        )

#Render de cada fila de la tabla
def render_row(pos, username, score, highlight=False):
    return rx.hstack(
        rx.text(
            f"{pos}.",
            width="25px",
            font_size="0.85em",
            color=rx.cond(highlight, "white", Colors.GOLD),
        ),
        rx.text(username, font_size="0.85em", color="white", flex="1", text_align="left"),
        rx.box(
            rx.text(f"{score}", font_weight="bold", color=Colors.GOLD, font_size="0.85em"),
            padding="1px 8px",
            background_color=Colors.LEADERBOARD_SCORE_BG,
            border_radius="6px",
            border=f"1px solid {Colors.GOLD}",
            min_width="50px",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        width="100%",
        padding="4px 8px",
        background_color=rx.cond(highlight, Colors.LEADERBOARD_ROW_HIGHLIGHT, Colors.LEADERBOARD_ROW_BG),
        border_radius="6px",
    )
