import reflex as rx
from QQSM.states.register_state import RegisterState
from QQSM.styles.styles import *
from QQSM.pages.components import *

#Título de la página
TITLE: str = "¿QUIÉN QUIERE SER MILLONARIO?"

#Título del formulario
FORM_TITLE: str = "¡REGÍSTRATE!"

#Texto del botón para enviar el formulario
SUBMIT_BTN_TEXT: str = "Registrar usuario"

#Página reflex que genera la interfaz del registro de usuario
@rx.page("/register", on_load=RegisterState.clear_message())
def register_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.box(
                rx.text(TITLE, class_name="title-style"),
                height="10vh",
                display="flex",
                align_items="center",
                justify_content="center"
            ),
            rx.box(
                render_form(FORM_TITLE, SUBMIT_BTN_TEXT, RegisterState.register_message, RegisterState.handle_register),
                background_color=Colors.DARK_BLUE,
                padding="20px",
                border_radius="10px",
                border=f"2px solid {Colors.GOLD}",
                width="33vw",
                height="85vh",
                display="flex",
                align_items="center",
                justify_content="center",
                overflow="hidden",
            ),
            spacing="5",
            align="center",
        ),
        width="100vw",
        height="100vh",
        background_image=qqsm_background,
        background_position="center",
        background_repeat="no-repeat",
        display="flex",
        align_items="center",
        justify_content="center",
        overflow="hidden",
    )

