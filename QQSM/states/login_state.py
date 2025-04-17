import reflex as rx
from QQSM.auth import login_user
from db.database import SessionLocal


class LoginState(rx.State):
    login_message: str = ""
    username: str = ""
    password: str = ""
    is_authenticated: bool = False

    @rx.event
    def clear_message(self):
        self.login_message = ""

    @rx.event
    def clear_and_redirect(self):
        self.login_message = ""
        yield
        return rx.redirect("/register")

    @rx.event
    def handle_login(self, form_data: dict):
        """Evento que procesa el formulario de inicio de sesión."""
        username = form_data["usuario"]
        password = form_data["password"]

        if not username or not password:
            self.login_message = "❌ Por favor, complete ambos campos"
            return

        db = SessionLocal()
        try:
            if login_user(username, password, db):
                # datos de sesión
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
