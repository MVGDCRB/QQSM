import reflex as rx
from QQSM.auth import login_user
from db.database import SessionLocal

#Estado reflex de login_page que genera la lógica del login

class LoginState(rx.State):
    #Mensaje de feedback durante el login
    login_message: str = ""
    #Nombre introducido por el usuario
    username: str = ""
    #Contraseña introducida por el usuario
    password: str = ""
    #True si el login se efectua correctamente
    is_authenticated: bool = False

    #Función que vacía el mensaje de feedback
    @rx.event
    def clear_message(self):
        self.login_message = ""

    #Evento que procesa el formulario de inicio de sesión.
    @rx.event
    def handle_login(self, form_data: dict):
        username = form_data["usuario"]
        password = form_data["password"]

        if (not username and password) or (not password and username) or username == "" and password == "":
            self.login_message = "❌ Por favor, complete ambos campos"
            return
        else:
            db = SessionLocal()
            try:
                if login_user(username, password):
                    self.username = username
                    self.password = password
                    self.is_authenticated = True
                    self.login_message = f"✅ Usuario '{username}' autenticado correctamente."
                    return rx.redirect("/menu")
                else:
                    self.login_message = "❌ Usuario o contraseña incorrectos."
            except Exception as e:
                self.login_message = f"❌ Error en la autenticación: {e}"
            finally:
                db.close()
