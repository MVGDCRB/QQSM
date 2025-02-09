import reflex as rx
import random

from rxconfig import config
from QQSM.auth import create_user, login_user
from db.database import init_db
from QQSM.pages.login_page import login_page 
from QQSM.pages.register_page import register_page 
from QQSM.pages.game_page import game_page 

#from QQSM.pages import register_page, login_page, game_page
from QQSM.state import State

# Inicializa la base de datos y crea las tablas antes de ejecutar Reflex  
init_db()


def index() -> rx.Component:
    return rx.cond(State.is_authenticated, game_page(), register_page()) #si esta registrado te manda al index sino al login


app = rx.App()

app.add_page(index)
app.add_page(register_page, route="registro")
app.add_page(login_page, route="login")  # Ruta como string y la función como segundo parámetro

if __name__ == "__main__":
    app.run()