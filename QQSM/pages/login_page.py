import reflex as rx
from QQSM.states.login_state import LoginState


@rx.page("/login")
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
                    rx.button("Volver", on_click=rx.redirect("/welcome"), class_name="hex-button"),
                    spacing="4",
                    align="center",
                ),
                on_submit=LoginState.handle_login, 
                reset_on_submit=True,
            ),
            rx.text(LoginState.login_message, class_name="error-message"),
            # background_color=Colors.DARK_BLUE,
            # padding="40px",
            # border_radius="10px",
            # box_shadow="0px 0px 15px rgba(255, 255, 255, 0.2)",
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
