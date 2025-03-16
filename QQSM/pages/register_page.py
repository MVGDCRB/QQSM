import reflex as rx
from QQSM.states.register_state import RegisterState

def register_page(): 
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
                    rx.button("Registrar usuario", type="submit", class_name="custom-button"),
                    rx.button("Ya tengo cuenta", on_click=rx.redirect("/login"), class_name="custom-button"),
                    spacing="5",
                    align="center",
                ),
                on_submit=RegisterState.handle_register,  
                reset_on_submit=True,
            ),
            rx.text(RegisterState.register_message, class_name="error-message"),
            background_color="#1E3A5F",  # Fondo azul oscuro
            padding="40px",
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

