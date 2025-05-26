import reflex as rx
from QQSM.states.register_state import RegisterState
from QQSM.states.login_state import LoginState
from QQSM.pages.components import*
from QQSM.styles.styles import*

TITLE: str = "¿QUIÉN QUIERE SER MILLONARIO?"

#Página reflex que genera la interfaz de la página de bienvenida
@rx.page("/welcome")
def welcome_page() -> rx.Component:
    return rx.center(
        rx.box(
            rx.form(
                rx.vstack(
                    render_header(TITLE),
                    rx.button("Iniciar Sesión", on_click=rx.redirect("/login"),class_name="hex-button subheader-style"),
                    rx.button("Registrarse", on_click=rx.redirect("/register"),class_name="hex-button subheader-style"),
                    spacing="9",
                    align="center",
                ),
            ),
        ),
        width="100vw",
        height="100vh",
        background_image=qqsm_background,
        background_position="center",
        background_repeat="no-repeat",
        display="flex",
        align_items="center",
        justify_content="center",
    )
