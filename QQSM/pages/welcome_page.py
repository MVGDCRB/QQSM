import reflex as rx
from QQSM.styles.colors import Colors
from QQSM.states.register_state import RegisterState
from QQSM.states.login_state import LoginState


@rx.page("/welcome")
def welcome_page():
    return rx.center(
        rx.box(
            rx.form(
                rx.vstack(

                    rx.button("Iniciar Sesión", on_click=LoginState.clear_message,
                              class_name="hex-button"),
                    rx.button("Registrarse", on_click=RegisterState.clear_message,
                              class_name="hex-button"),
                    spacing="4",
                    align="center",
                ),
            ),
            background_color=Colors.DARK_BLUE,
            padding="40px",
            border_radius="10px",
            box_shadow="0px 0px 15px rgba(255, 255, 255, 0.2)",
        ),
        width="100vw",
        height="100vh",
        background_color=Colors.DARK_BLUE,
        background_image="url('/welcome_fondo.jpg')",  # Ruta relativa a assets/
        background_size="cover",
        background_position="center",
        background_repeat="no-repeat",
        display="flex",
        align_items="center",
        justify_content="center",
    )
