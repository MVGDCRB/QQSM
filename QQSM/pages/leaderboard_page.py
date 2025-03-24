import reflex as rx
from db.database import SessionLocal
from QQSM.auth import get_top_10_users
from QQSM.auth import get_user_leaderboard

# Leaderboard Page
def leaderboard_page():

    top_users = get_top_10_users()
    user = get_user_leaderboard("aaa")#Hay que pasar el usuario actual (hay que meter cookies)

    print(top_users)
    print(user)

    return rx.center(
        rx.vstack(
            rx.text("Leaderboard", font_size="2em"),
            rx.button("Volver al menu", on_click=rx.redirect("/menu")),
        ),
    )
