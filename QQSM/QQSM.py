import reflex as rx
import random

from rxconfig import config
from QQSM.auth import create_user, login_user
from db.database import init_db
from QQSM.pages import register_page, login_page, game_page
from QQSM.state import State

# Inicializa la base de datos y crea las tablas antes de ejecutar Reflex  
init_db()


def index() -> rx.Component:
    return rx.cond(State.is_authenticated, game_page.game_page(), register_page.register_page()) #si esta registrado te manda al index sino al login


app = rx.App()
app.add_page(index)
