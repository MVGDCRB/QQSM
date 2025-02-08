import reflex as rx

from db.database import SessionLocal
from QQSM.auth import login_user, create_user

class State(rx.State):

    form_data: dict = {}

    @rx.event
    def handle_login(self, form_data : dict):
        """Función de inicio de sesión del usuario"""
        #hacer funcion que redirija si todo esta bien a la pagina del juego

    @rx.event
    def handle_register(self, form_data : dict):        
        """Función de registro del usuario"""
        db = SessionLocal() #guardo la sesionLocal en una variable
        try:
            create_user(form_data["usuario"], form_data["password"], db)  # se pasa db junto al usuario y contraseña hasheada
            print("✅ Usuario registrado con éxito")
        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")
        finally:
            db.close()

    quiz_questions = [
        ("¿Cuál es la capital de Francia?", ["Madrid", "Berlín", "París", "Lisboa"], 2),
        ("¿Cuántos planetas hay en el sistema solar?", ["7", "8", "9", "10"], 1),
        ("¿Quién escribió 'Don Quijote de la Mancha'?", ["Cervantes", "Lorca", "Quevedo", "Góngora"], 0),
        ("¿Cuál es el resultado de 5 + 7?", ["10", "11", "12", "13"], 2),
        ("¿Qué gas respiramos principalmente?", ["Oxígeno", "Nitrógeno", "Dióxido de carbono", "Helio"], 0),
    ]

    totalPreguntas = len(quiz_questions)
    show_page_one: bool = True
    textoPregunta: str = None
    tituloOpciones: list[str] = ["A)", "B)", "C)", "D)"]
    textoOpciones: list[str] = []
    opcionCorrecta: int = -1
    numRonda: int = 1

    # Variables de usuario
    username: str = ""
    password: str = ""
    is_authenticated: bool = False

    def set_username(self, username: str):
        """Método para actualizar el estado de username"""
        self.username = username

    def set_password(self, password: str):
        """Método para actualizar el estado de la contraseña"""
        self.password = password

    def toggle_page(self):
        self.show_page_one = not self.show_page_one

    def seleccionarPregunta(self):
        self.textoPregunta, self.textoOpciones, self.opcionCorrecta = self.quiz_questions[self.numRonda - 1]

    def verificar_respuesta(self, seleccion: int):
        if seleccion == self.opcionCorrecta:
            print("✅ Respuesta correcta")
            self.numRonda += 1

            if self.numRonda == self.totalPreguntas:
                self.numRonda = 1
                self.toggle_page()
            else:
                self.seleccionarPregunta()
        else:
            print("❌ Respuesta incorrecta")
            self.toggle_page()
            self.numRonda = 1
