import reflex as rx
from QQSM.states.register_state import RegisterState
from QQSM.states.login_state import LoginState


@rx.page("/welcome")
def welcome_page():
    return rx.center(
        rx.box(
            rx.form(
                rx.vstack(
                    rx.text("¿QUIÉN QUIERE SER MILLONARIO?", class_name="title-style"),
                    rx.button("Iniciar Sesión", on_click=LoginState.clear_message,
                              class_name="hex-button"),
                    rx.button("Registrarse", on_click=RegisterState.clear_message,
                              class_name="hex-button"),
                    spacing="9",
                    align="center",
                ),
            ),

        ),
        width="100vw",
        height="100vh",
        background_image="url('/welcome_fondo.jpg')",  # Ruta relativa a assets/
        background_size="cover",
        background_position="center",
        background_repeat="no-repeat",
        display="flex",
        align_items="center",
        justify_content="center",
    )
