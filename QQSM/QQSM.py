import reflex as rx
import random

from rxconfig import config
from db.database import init_db
from QQSM.pages.login_page import login_page 
from QQSM.pages.register_page import register_page 
from QQSM.pages.menu_page import menu_page 
from QQSM.pages.game_page import game_page


#from QQSM.pages import register_page, login_page, game_page
from QQSM.states.state import State

# Inicializa la base de datos y crea las tablas antes de ejecutar Reflex  
init_db()


def index() -> rx.Component:
    return rx.cond(State.is_authenticated, menu_page(), register_page()) #si esta registrado te manda al index sino al login


app = rx.App()

app.add_page(index, route="/")
app.add_page(register_page, route="/registro")
app.add_page(login_page, route="/login")  # Ruta como string y la función como segundo parámetro
app.add_page(menu_page, route="/menu")
app.add_page(game_page, route="/game")

if __name__ == "__main__":
    app.run()