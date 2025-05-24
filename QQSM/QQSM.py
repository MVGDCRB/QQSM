import reflex as rx
from db.database import init_db
import QQSM.pages as qqsm_pages

# Inicializa la base de datos y crea las tablas antes de ejecutar Reflex
init_db()

welcome_page = qqsm_pages.welcome_page.welcome_page

#La página inicial es la de bienvenida
def index() -> rx.Component:
    return welcome_page()

#Se crea el objeto app con sus dependencias .css
app = rx.App(
    stylesheets=[
        "/css/styles.css",
    ],
)

#Se agrega la pagina inicial a la raiz
app.add_page(index, route="/")


#punto de entrada para ejecutar la app
if __name__ == "__main__":
    app.run()
