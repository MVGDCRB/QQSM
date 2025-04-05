import reflex as rx
from QQSM.states.state import State

# User Profile Page
def user_page():

    user = State.username if State.username else "Usuario no identificado"
    state = State()

    print(user)


    return rx.center(
        rx.vstack(
            rx.text(f"Perfil Usuario: {user}", font_size="2em"),
            rx.button("Volver al menu", on_click=rx.redirect("/menu")),
        ),
    )
