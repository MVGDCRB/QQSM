import reflex as rx
from QQSM.auth import create_user
from db.database import SessionLocal

# state/register.py
class RegisterState(rx.State):
    # State handling here
    register_message: str = ""

    @rx.event
    def handle_register(self, form_data : dict):        
        """Función de registro del usuario"""
        db = SessionLocal() #guardo la sesionLocal en una variable
        try:
            create_user(form_data["usuario"], form_data["password"], db)  # se pasa db junto al usuario y contraseña hasheada
            self.register_message = f"✅ Usuario registrado con éxito."
            print("✅ Usuario registrado con éxito")
            return rx.redirect("/login")  # Redirige a la página de login después de 2 segundos

        except Exception as e:
            self.register_message = f"❌ El nombre de usuario ya está en uso"
        finally:
            db.close()