import reflex as rx
from QQSM.states.register_state import RegisterState
from QQSM.states.login_state import LoginState
from QQSM.pages.components import*

TITLE: str = "¿QUIÉN QUIERE SER MILLONARIO?"

#Página reflex que genera la interfaz de la página de bienvenida
@rx.page("/welcome")
def welcome_page():
    return rx.center(
        rx.box(
            rx.form(
                rx.vstack(
                    render_game_header(TITLE),
                    rx.button("Iniciar Sesión", on_click=LoginState.clear_message,class_name="hex-button"),
                    rx.button("Registrarse", on_click=RegisterState.clear_message,class_name="hex-button"),
                    spacing="9",
                    align="center",
                ),
            ),
        ),
        width="100vw",
        height="100vh",
        background_image="url('/welcome_fondo.jpg')",
        background_size="cover",
        background_position="center",
        background_repeat="no-repeat",
        display="flex",
        align_items="center",
        justify_content="center",
    )
