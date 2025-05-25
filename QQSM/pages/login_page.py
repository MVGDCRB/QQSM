import reflex as rx
from QQSM.states.login_state import LoginState
from QQSM.styles.colors import Colors
from QQSM.pages.components import*

#Título de la página
TITLE: str = "¿QUIÉN QUIERE SER MILLONARIO?"

#Título del formulario
FORM_TITLE: str = "¡INICIA SESIÓN!"

#Texto del botón para enviar el formulario
SUBMIT_BTN_TEXT: str = "Iniciar sesión"

#Página reflex que genera la interfaz del login de usuario
@rx.page("/login")
def login_page():
    return rx.center(
        rx.vstack(
            rx.text(TITLE, class_name="title-style"),
            rx.box(
                render_form(FORM_TITLE, SUBMIT_BTN_TEXT, LoginState.login_message, LoginState.handle_login),
                background_color=Colors.DARK_BLUE,
                padding="20px",
                border_radius="10px",
                border=f"2px solid {Colors.GOLD}",
                box_shadow="0px 0px 15px rgba(255, 255, 255, 0.2)",
                width="33vw",
                height="80vh",
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
        background_image="url('/welcome_fondo.jpg')",
        background_size="cover",
        background_position="center",
        background_repeat="no-repeat",
        display="flex",
        align_items="center",
        justify_content="center",
        overflow="hidden",
    )
