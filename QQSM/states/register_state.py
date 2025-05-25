import reflex as rx
from QQSM.auth import create_user
from db.database import SessionLocal


class RegisterState(rx.State):
    register_message: str = ""

    @rx.event
    def clear_message(self):
        self.register_message = ""
        return rx.redirect("/register")

    @rx.event
    def handle_register(self, form_data: dict):
        """Función de registro del usuario"""
        db = SessionLocal()  # guardo la sesionLocal en una variable
        try:
            if form_data["usuario"] != "" and form_data["password"] != "":
                # se pasa db junto al usuario y contraseña hasheada
                create_user(form_data["usuario"], form_data["password"], db)
                self.register_message = f"✅ Usuario registrado con éxito."
                return rx.redirect("/login")  # Redirige a la página de login después de 2 segundos

        except Exception as e:
            self.register_message = f"❌ El nombre de usuario ya está en uso, {e}"
        finally:
            db.close()
