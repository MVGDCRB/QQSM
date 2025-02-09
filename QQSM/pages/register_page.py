import reflex as rx

from QQSM.state import State


def register_page(): 
    return rx.center(
        rx.form(
            rx.vstack(
                rx.text("Registrarse", font_size="2em"),
                rx.input(
                    placeholder="Usuario", 
                    name = "usuario"
                    ),  
                rx.input(
                    placeholder="Password",
                    type= "password",
                    name = "password"
                    ),              
                rx.button("Registrar usuario", type = "submit"),
                rx.divider(),
                rx.button("Ya tengo cuenta", on_click=rx.redirect("/login"))#hacer redireccion a login_page
            ),
            on_submit=State.handle_register, 
            reset_on_submit=True,
        ),
    )   