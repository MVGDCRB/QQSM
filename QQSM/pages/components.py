import reflex as rx
from QQSM.states.game_state import GameState
from QQSM.styles.colors import Colors

#Biblioteca de componentes reflex con estilos .css customizados

#Botón en forma de X con estilo css customizado que vuelve al menú principal
def render_exit_button() -> rx.Component:
    return rx.button(
        "✖",
        on_click=rx.redirect("/menu"),
        class_name="menu-exit-button"
    )

#Panel de texto que escribe un título centrado con estilo css customizado
def render_game_header(text: str) -> rx.Component:
    return rx.box(
        rx.text(
            text,
            class_name="title-style",
            margin="0px"
        ),
        width="100%",
        padding="0px",
        text_align="center"
    )

#Botón customizado con forma de flecha que dispara el evento de GameState next_round() para pasar a la siguiente pregunta, si se cumple la condicion show
def render_next_button(show: bool) -> rx.Component:
    return rx.cond(
        show,
        rx.button(
            "➜",
            on_click=GameState.next_round.debounce(1000),
            class_name="next-arrow-button"
        )
    )

#Función auxiliar de render_progress_indicator
#Dado un número de pasos de transición y un index para uno de esos pasos se calcula el color intermedio entre el verde y el rojo correspondiente para representar la dificultad
def get_gradient_color(index: int, steps: int) -> str:
    factor = index / (steps - 1) if steps > 1 else 0
    r = int(factor * 255)
    g = int((1 - factor) * 255)
    b = 0
    return f"rgb({r},{g},{b})"

#Panel de círculos numerados que indican el grado de dificultad de las preguntas respondidas hasta el momento actual, incluida la actual con un color entre verde y rojo
def render_progress_indicator(steps: int) -> rx.Component:
    number = GameState.number_question

    return rx.hstack(
        *[
            rx.box(
                # Numeros de pregunta
                rx.text(
                    ((number - 1) // steps) * steps + (i + 1),
                    font_size="14px",
                    color="gold",
                    text_align="center",
                ),
                # circulos
                rx.box(
                    class_name=rx.cond(
                        i == (number - 1) % steps,
                        "progress-circle current",
                        "progress-circle",
                    ),
                    background_color=rx.cond(
                        i <= (number - 1) % steps,
                        get_gradient_color(i, steps),
                        "gray",
                    ),
                ),
                display="flex",
                flex_direction="column",
                align_items="center",
            )
            for i in range(steps)
        ],
        spacing="6",
        align="center",
        justify="center",
        class_name="progress-container",
        width="100%",
        margin_bottom="5px",
    )

#Panel de texto hexagonal que contiene el texto del enunciado de una pregunta.
def render_question_title(question_title: str) -> rx.Component:
    return rx.box(
        rx.text(
            question_title,
            white_space="normal",
            word_break="break-word",
            color="white",
            text_align="center",
            class_name="custom-title",
        ),
        width="70%",
        padding="5px",
        border_radius="8px",
    )

#Panel circular que muestra con una imagen el tema de la pregunta actual. Cuando se hace hover sobre el muestra el texto del tema en cuestión.
def render_question_topic(theme: str) -> rx.Component:
    return rx.box(
        class_name="theme-icon image",
        background_image=f"url('/themes/{theme}.png')",
        **{"data-theme": theme},
        width="100px",
        height="100px",
        flex_shrink="0",
    )

#Doble panel circular de botones temáticos. El primero panel que se pulse establece el tema de la pregunta para esa ronda.
def render_topic_choser(theme1: str, theme2:str) -> rx.Component:

    def icon_button(theme) -> rx.Component:
        return rx.button(
            render_question_topic(theme),
            on_click=GameState.set_theme(theme),
            disabled=GameState.enable_topic,
            style={"padding": "0", "border": "none", "background": "none"},
        )

    return rx.hstack(
        icon_button(theme1),
        icon_button(theme2),
        spacing="5",
        align="center",
        justify="center",
    )

#Cuadrícula 2x2 de botones hexagonales para mostras las cuatro posibles respuestas al enunciado de la pregunta. Dan feedback de validación a la respuesta tras ser pulsados.
def render_answer_options() -> rx.Component:
    return rx.grid(
        *[
            rx.button(
                f"{letter}) {getattr(GameState, f'option_{letter.lower()}')}",
                width="100%",
                font_size="14px",
                white_space="normal",
                word_break="break-word",
                height="auto",
                min_height="50px",
                class_name=GameState.button_classes[letter],
                on_click=lambda le=letter: GameState.validate_answer(le),
                disabled=GameState.chosen_answer
            )
            for letter in ["A", "B", "C", "D"]
        ],
        columns="2",
        spacing="4",
        width="70%",
        align_items="center",
        justify_content="center",
        margin_top="10px",
    )

#Gráfico de barras que muestra el voto del público para las 4 opciones de respuesta para una pregunta dada
def render_public_chart() -> rx.Component:
    return rx.hstack(
        rx.foreach(
            GameState.public_items,
            lambda item, idx: rx.vstack(
                # Porcentaje de voto
                rx.text(f"{item[1]}%", font_size="14px", color="white"),
                # Barra
                rx.box(
                    width="30px",
                    height=f"{item[1] * 2}px",
                    background_color=Colors.GOLD,
                    border_radius="5px",
                ),
                # Letra de la opción debajo de la barra
                rx.text(item[0], font_size="14px", color="white"),
                align="center",
                spacing="2",
            )
        ),
        width="25vw",
        height="33vh",
        spacing="3",
        align="end",
        justify="end",
    )

#Panel de texto que se muestra cuando se invoca el comodín de la llamada con la respuesta de la IA
def render_call_box() -> rx.Component:
    return rx.box(
        rx.center( 
                rx.text(
                    GameState.call_text,
                    font_size="1.1em",
                    color="white",
                    text_align="left",
                    white_space="pre-wrap",
                    word_break="break-word",
                )
        ),
        width="220px",
        height="450px",
        background_color="#111827",
        padding="20px",
        border_radius="30px",
        border=f"2px solid {Colors.GOLD}",
        box_shadow="0 0 20px rgba(255, 215, 0, 0.5)",
        overflow_y="auto",
        display="flex",
        align_items="center",
        justify_content="center",
    )

#Botón customizado para representar el comodín de la llamada
def render_joker_call() -> rx.Component:
    return rx.button(
        rx.box(
            class_name="theme-icon image",
            background_image="url('/buttons/call.png')",
            **{"data-theme": "Llamada"},
            width="60px",
            height="60px",
        ),
        on_click=GameState.use_call_option,
        disabled=GameState.call_used | GameState.chosen_answer,
        style={"padding": "0", "border": "none", "background": "none"},
    )

#Botón customizado para representar el comodín del 50-50
def render_joker_fifty() -> rx.Component:
    return rx.button(
        rx.box(
            class_name="theme-icon image",
            background_image="url('/buttons/fifty.png')",
            **{"data-theme": "50:50"},
            width="60px",
            height="60px",
        ),
        on_click=GameState.use_fifty_option,
        disabled=GameState.fifty_used | GameState.chosen_answer,
        style={"padding": "0", "border": "none", "background": "none"},
        
    )

#Botón customizado para representar el comodín del público
def render_joker_public() -> rx.Component:
    return rx.button(
        rx.box(
            class_name="theme-icon image",
            background_image="url('/buttons/public.png')",
            **{"data-theme": "Público"},
            width="60px",
            height="60px",
        ),
        on_click=GameState.use_public_option,
        disabled=GameState.public_used | GameState.chosen_answer,
        style={"padding": "0", "border": "none", "background": "none"},
        
    )


#Fragmento de texto que se muestra cuando es necesario un feedback adicional al usuario, como errores
def render_feedback_line() -> rx.Component:
    return rx.cond(
        GameState.feedback != "",
        rx.box(
            rx.text(
                GameState.feedback,
                font_size="16px",
                color="white",
                text_align="center"
            ),
            width="100%",
            padding="10px",
            position="absolute",
            bottom="0px",
            text_align="center"
        )
    )

# Componente parametrizado para mostrar un logo de IA según tema
def render_ia_icon(ia_name: str) -> rx.Component:
    image_url = f"/ias/{ia_name}.png"
    return rx.box(
        class_name="theme-icon image",
        background_image=f"url('{image_url}')",
        **{"data-theme": ia_name},
        width="100px",
        height="100px",
    )

#Botón circular que muestra render_ia_icon de la IA correspondiente y lanza la ruta al clicar.
def render_ia_button(ia_name: str, route: str) -> rx.Component:
    return rx.button(
        render_ia_icon(ia_name),
        on_click=GameState.initialize_game(route),
        style={"padding": "0", "border": "none", "background": "none"},
    )

#Panel que muestra tres render_ia_button que permiten elegir a la IA rival
def render_ia_chooser() -> rx.Component:
    
    return rx.hstack(
        render_ia_button("deepSeek", "/deepSeekIA"),
        render_ia_button("openAI", "/openAI"),
        render_ia_button("llamaIA", "/llamaIA"),
        spacing="6",
        align="center",
        justify="center",
        width="100%",
        margin_top="10px",
    )


# Componente para mostrar el texto 'VS' con efecto degradado y sombra.
def render_vs_text() -> rx.Component:
    return rx.text(
        "VS",
        font_size="4em",
        font_weight="bold",
        font_family="Impact, sans-serif",
        color="transparent",
        background="linear-gradient(180deg, #FFD700, #FF4500, #8B0000)",
        background_clip="text",
        text_shadow=(
            "1px 1px 1px black, "
            "0 0 4px #FF4500, "
            "0 0 8px #FF8C00"
        ),
        margin="0 20px",
        height="100px",
        line_height="100px",
        display="flex",
        align_items="center",
        justify_content="center",
    )


