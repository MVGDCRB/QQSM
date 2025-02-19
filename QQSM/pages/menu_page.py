import reflex as rx
from QQSM.states.game_state import GameState

def menu_page():
    return rx.center(
        rx.vstack(
            rx.text("Menu", font_size="2em"),
            rx.button("Jugar", on_click=GameState.initialize_game),
            rx.divider(),
            rx.button("Marcadores"),
            rx.divider(),
            rx.button("Perfil Usuario"),
            rx.divider(),
        ),
    )