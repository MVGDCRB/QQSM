import reflex as rx

def menu_page():
    return rx.center(
        rx.vstack(
            rx.text("Menu", font_size="2em"),
            rx.button("Jugar", on_click=rx.redirect("/game")),
            rx.divider(),
            rx.button("Marcadores"),
            rx.divider(),
            rx.button("Perfil Usuario"),
            rx.divider(),
        ),
    )