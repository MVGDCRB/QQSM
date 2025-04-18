import reflex as rx
from db.database import init_db
from QQSM.pages.login_page import login_page 
from QQSM.pages.register_page import register_page 
from QQSM.pages.menu_page import menu_page 
from QQSM.pages.game_page import game_page
from QQSM.pages.leaderboard_page import leaderboard_page
from QQSM.pages.user_page import user_page
from QQSM.pages.endless_page import endless_page
from QQSM.pages.theme_page import theme_page
from QQSM.pages.wellcome_page import wellcome_page


# Inicializa la base de datos y crea las tablas antes de ejecutar Reflex  
init_db()


def index() -> rx.Component:
    return rx.cond(True, wellcome_page(), wellcome_page())


app = rx.App(
    stylesheets=[
        "/css/styles.css",  # This path is relative to assets/
    ],
)

app.add_page(index, route="/")
app.add_page(wellcome_page, route="/wellcome")
app.add_page(register_page, route="/register")
app.add_page(login_page, route="/login")  # Ruta como string y la función como segundo parámetro
app.add_page(menu_page, route="/menu")
app.add_page(game_page, route="/game")
app.add_page(leaderboard_page, route="/leaderboard")
app.add_page(user_page, route="/user_page")
app.add_page(endless_page, route="/endless")
app.add_page(theme_page, route="/theme")


if __name__ == "__main__":
    app.run()
