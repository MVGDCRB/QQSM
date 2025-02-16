import reflex as rx

from db.database import SessionLocal
from QQSM.auth import login_user, create_user

class State(rx.State):

    form_data: dict = {}

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

    