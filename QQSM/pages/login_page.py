import reflex as rx
from QQSM.states.login_state import LoginState

def login_page():
    return rx.center(
        rx.box(
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Usuario", 
                        name="usuario",
                        class_name="custom-input"
                    ),  
                    rx.input(
                        placeholder="Contraseña",
                        type="password",
                        name="password",
                        class_name="custom-input"
                    ),              
                    rx.button("Iniciar Sesión", type="submit", class_name="hex-button"),
                    rx.button("No tengo cuenta", on_click=LoginState.clear_and_redirect, class_name="hex-button"),
                    spacing="4",
                    align="center",
                ),
                on_submit=LoginState.handle_login, 
                reset_on_submit=True,
            ),
            rx.text(LoginState.login_message, class_name="error-message"),
            background_color="#1E3A5F",  # Fondo azul oscuro
            padding="40px",
            border_radius="10px",
            box_shadow="0px 0px 15px rgba(255, 255, 255, 0.2)",
        ),
        width="100vw",
        height="100vh",
        background_color="#1E3A5F",  # Fondo azul oscuro global
        display="flex",
        align_items="center",
        justify_content="center",
    )
