import reflex as rx
from QQSM.states.register_state import RegisterState
from QQSM.styles.colors import Colors


@rx.page("/register")
def register_page():
    return rx.center(
        rx.vstack(
            rx.text("¿QUIÉN QUIERE SER MILLONARIO?", class_name="title-style"),
            rx.box(
                rx.form(
                    rx.vstack(
                        rx.box(
                            rx.text(
                                "¡REGÍSTRATE!",
                                color=Colors.ORANGE_BORDER,
                                font_size="1.5em",
                                font_weight="bold",
                                text_transform="uppercase",
                                text_align="center",
                                letter_spacing="1px",
                                width="100%",
                            ),
                            height="20%",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            width="100%",
                        ),
                        rx.box(
                            rx.input(
                                placeholder="Usuario",
                                name="usuario",
                                class_name="custom-input",
                                width="100%",
                                margin_bottom="10%",  # separación entre inputs
                            ),
                            rx.input(
                                placeholder="Contraseña",
                                type="password",
                                name="password",
                                class_name="custom-input",
                                width="100%",
                            ),
                            height="30%",
                            display="flex",
                            flex_direction="column",
                            align_items="center",
                            justify_content="center",
                            width="100%",
                            margin_bottom="10%",  # separación del bloque siguiente
                        ),
                        rx.box(
                            rx.button(
                                "Registrar usuario",
                                type="submit",
                                class_name="hex-button",
                                width="100%",
                                margin_bottom="10%",  # separación entre botones
                            ),
                            rx.button(
                                "Volver",
                                on_click=rx.redirect("/welcome"),
                                class_name="hex-button",
                                width="100%",
                            ),
                            height="40%",
                            display="flex",
                            flex_direction="column",
                            align_items="center",
                            justify_content="center",
                            width="100%",
                        ),
                        rx.box(
                            rx.text(RegisterState.register_message, class_name="error-message"),
                            height="10%",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            width="100%",
                        ),
                        height="100%",
                        width="85%",
                        margin_left="auto",
                        margin_right="auto",
                        align="center",
                        justify="center",
                    ),
                    on_submit=RegisterState.handle_register,
                    reset_on_submit=True,
                    height="100%",
                    width="100%",
                    justify="center",
                    align="center",
                ),
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
