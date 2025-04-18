import reflex as rx
from QQSM.states.game_state import GameState
from QQSM.styles.colors import Colors


@rx.page("/menu")
def menu_page():
    return rx.center(
        rx.box(
            rx.vstack(
                rx.button("Modo Normal", on_click=GameState.initialize_game("/game"),
                          class_name="hex-button", width="300px"),
                rx.button("Modo Infinito", on_click=GameState.initialize_game("/endless"),
                          class_name="hex-button", width="300px"),
                rx.button("Modo Temas", on_click=GameState.initialize_game("/theme"),
                          class_name="hex-button", width="300px"),
                rx.button("Marcadores", on_click=rx.redirect("/leaderboard"),
                          class_name="hex-button", width="300px"),
                rx.button("Perfil Usuario", on_click=rx.redirect("/user_page"),
                          class_name="hex-button", width="300px"),
                spacing="6",  
                align="center",
            ),
            background_color=Colors.DARK_BLUE, 
            padding="50px",
            border_radius="10px",
            box_shadow="0px 0px 15px rgba(255, 255, 255, 0.2)",
            position="relative",
            width="fit-content"
        ),
        rx.box(
            rx.button("✖", on_click=rx.redirect("/wellcome"), class_name="menu-exit-button"),
            position="absolute",
            top="20px",
            left="20px"
        ),
        width="100vw",
        height="100vh",
        background_color=Colors.DARK_BLUE,
        display="flex",
        align_items="center",
        justify_content="center",
        position="relative",
        overflow="hidden"
    )
