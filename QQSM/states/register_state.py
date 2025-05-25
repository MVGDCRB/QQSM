import reflex as rx
from QQSM.auth import create_user
from db.database import SessionLocal

#Estado reflex de register_page que genera la lógica del registro de usuario

class RegisterState(rx.State):
    
    #Mensaje de feedback durante el registro del usuario
    register_message: str = ""

    #Función que vacía el mensaje de feedback y recarga la página
    @rx.event
    def clear_message(self):
        self.register_message = ""
        return rx.redirect("/register")

    #Evento que procesa el formulario de registro del usuario.
    @rx.event
    def handle_register(self, form_data: dict):
        db = SessionLocal()
        try:
            if form_data["usuario"] != "" and form_data["password"] != "":
                create_user(form_data["usuario"], form_data["password"], db)
                self.register_message = f"✅ Usuario registrado con éxito."
                return rx.redirect("/login")

        except Exception as e:
            self.register_message = f"❌ El nombre de usuario ya está en uso, {e}"
        finally:
            db.close()
