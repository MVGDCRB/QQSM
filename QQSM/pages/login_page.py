import reflex as rx
from QQSM.states.login_state import LoginState

def login_page():
    return rx.center(
        rx.form(
            rx.vstack(
                rx.text("Inicio Sesión", font_size="2em"),
                rx.input(
                    placeholder="Usuario", 
                    name = "usuario"
                    ),  
                rx.input(
                    placeholder="Password",
                    type= "password",
                    name = "password"
                    ),              
                rx.button("Login usuario", type = "submit"),
                rx.divider(),
                rx.button("No tengo cuenta", on_click=LoginState.clear_and_redirect()) #hacer redireccion a register_page

            ),
            on_submit=LoginState.handle_login, 
            reset_on_submit=True,
        ),
        rx.text(LoginState.login_message),  # Display the message
    )