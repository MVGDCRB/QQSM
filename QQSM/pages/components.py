import reflex as rx
from QQSM.states.game_state import GameState
from QQSM.styles.styles import Colors

#Biblioteca de componentes reflex con estilos .css customizados

#Botón en forma de X con estilo css customizado que vuelve al menú principal
def render_exit_button(route: str) -> rx.Component:
    return rx.button(
        "✖",
        on_click=rx.redirect(route),
        class_name="menu-exit-button"
    )

#Panel de texto que escribe un título centrado con estilo css customizado
def render_header(text: str) -> rx.Component:
    return rx.box(
        rx.text(
            text,
            class_name="title-style",
            margin="0px",
        ),
        width="100%",
        padding="0px",
        text_align="center"
    )

#Panel de texto que escribe un subtitulo text con formato customizado
def render_subheader(txt: str) -> rx.Component:
    return rx.text(
        txt,
        class_name="subheader-style",
        width="100%"
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

#Componente customizado circular que toma como background image la imagen del directorio /module/submodule y muestra text cuando se realiza hover sobre el icono
def render_circular_icon(module:str, submodule: str, text: str):
    return rx.box(
        class_name="theme-icon image",
        background_image=f"url('/{module}/{submodule}.png')",
        **{"data-theme": text},
        width="100px",
        height="100px",
        flex_shrink="0",
    )

#Panel circular que muestra con una imagen el tema de la pregunta actual. Cuando se hace hover sobre el muestra el texto del tema en cuestión.
def render_question_topic(theme: str) -> rx.Component:
    return render_circular_icon("themes", theme, theme)

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
    return render_circular_icon("ias", ia_name, ia_name)

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

#Dado un titulo, un texto de submit, un mensaje dinámico de feedback y un evento de submit, se genera un formulario
def render_form(form_title: str, submit_btn_txt: str, feedback_message: str, on_submit_event)-> rx.Component:
    return rx.form(
        rx.vstack(
            rx.box(
                render_subheader(form_title),
                height="20%",
                display="flex",
                align_items="center",
                justify_content="center",
                width="100%",
            ),
            render_user_input(),
            rx.box(
                render_submit_button(submit_btn_txt),
                render_return_button("Volver","/welcome"),
                height="40%",
                display="flex",
                flex_direction="column",
                align_items="center",
                justify_content="center",
                width="100%",
            ),
            render_feedback_message(feedback_message),
            height="100%",
            width="85%",
            margin_left="auto",
            margin_right="auto",
            align="center",
            justify="center",
        ),
        on_submit=on_submit_event,
        reset_on_submit=True,
        height="100%",
        width="100%",
        justify="center",
        align="center",
    )

#Componente auxiliar del formulario con los dos campos de texto input usuario y contraseña
def render_user_input()-> rx.Component:
    return rx.box(
                rx.input(
                    placeholder="Usuario",
                    name="usuario",
                    class_name="custom-input",
                    width="100%",
                    margin_bottom="10%",
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
                margin_bottom="10%",
            )

#Botón auxiliar del formulario que carga route cuando es pulsado
def render_return_button(txt:str, route: str)-> rx.Component:
    return rx.button(
                    txt,
                    on_click=rx.redirect(route),
                    class_name="hex-button subheader-style",
                    width="100%",
                )

#Botón auxiliar del formulario que envia sus campos cuando es pulsado
def render_submit_button(btn_txt: str)-> rx.Component:
    return rx.button(
                    btn_txt,
                    type="submit",
                    class_name="hex-button subheader-style",
                    width="100%",
                    margin_bottom="10%",
                )

#Mensaje de texto auxiliar del formulario que da contexto sobre el formulario en tiempo real
def render_feedback_message(message:str)-> rx.Component:
    return rx.box(
                rx.text(message, class_name="error-message"),
                height="10%",
                display="flex",
                align_items="center",
                justify_content="center",
                width="100%",
            )
#Botón circular de redirección a route que toma su fondo de /buttons/image y muestra text cuando se hace hover sobre el
def render_redirect_circular_button(text: str, image:str, route: str) -> rx.Component:
    return rx.button(
        render_circular_icon("buttons", image, text),
        on_click=rx.redirect(route)
    )

#Botón customizado hexagonal que inicializa el modo de juego route y presenta el texto txt
def render_game_mode_button(txt:str, route:str) -> rx.Component:
    return rx.button(
        txt,
        on_click=GameState.initialize_game(route),
        class_name="hex-button subheader-style",
        width="300px",
        margin_bottom="10%",
    )