import reflex as rx
from QQSM.states.game_state import GameState

def menu_page():
    return rx.center(
        rx.box(
            rx.vstack(
                rx.button("Modo Normal", on_click=GameState.initialize_game("/game"), class_name="custom-button", width="300px"),
                rx.button("Modo Infinito", on_click=GameState.initialize_game("/endless"), class_name="custom-button", width="300px"),
                rx.button("Marcadores", on_click = rx.redirect("/leaderboard"), class_name="custom-button", width="300px"),
                rx.button("Perfil Usuario", class_name="custom-button", width="300px"),
                spacing="9",  
                align="center",
            ),
            background_color="#1E3A5F", 
            padding="50px",
            border_radius="10px",
            box_shadow="0px 0px 15px rgba(255, 255, 255, 0.2)",  
        ),
        width="100vw",
        height="100vh",
        background_color="#1E3A5F",  
        display="flex",
        align_items="center",
        justify_content="center",
    )
