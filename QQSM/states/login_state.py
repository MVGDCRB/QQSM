import reflex as rx
from QQSM.auth import login_user
from db.database import SessionLocal
from QQSM.states.state import State

class LoginState(rx.State):
    # State variables
    login_message: str = ""
    
    @rx.event
    def clear_message(self):
        self.login_message = ""

    @rx.event
    def clear_and_redirect(self):
        self.login_message = ""
        return rx.redirect("/registro")
        
    @rx.event
    def handle_login(self, form_data: dict):
        username = form_data["usuario"]
        password = form_data["password"]
        
        if not username or not password:
            self.login_message = "❌ Por favor, complete ambos campos"
            return
            
        db = SessionLocal()
        try:
            if login_user(username, password, db):
                State.is_authenticated = True
                self.login_message = f"✅ Usuario '{username}' autenticado correctamente."
                return rx.redirect("/game")
            else:
                self.login_message = "❌ Usuario o contraseña incorrectos."
        except Exception as e:
            self.login_message = f"❌ Error en la autenticación: {str(e)}"
        finally:
            db.close()