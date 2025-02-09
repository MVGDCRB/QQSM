import reflex as rx
from QQSM.states.register_state import RegisterState

def register_page(): 
    return rx.center(
        rx.form(
            rx.vstack(
                rx.text("Registrarse", font_size="2em"),
                rx.input(
                    placeholder="Usuario", 
                    name="usuario"
                ),  
                rx.input(
                    placeholder="Password",
                    type="password",
                    name="password"
                ),              
                rx.button("Registrar usuario", type="submit"),
                rx.divider(),
                rx.button("Ya tengo cuenta", on_click=rx.redirect("/login"))  # Redirección al login page
            ),
            on_submit=RegisterState.handle_register,  # Referencia a la función sin paréntesis
            reset_on_submit=True,
        ),
        rx.text(RegisterState.register_message),  # Display the message

    )   

