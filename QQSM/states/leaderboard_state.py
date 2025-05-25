import reflex as rx
from QQSM.auth import get_top_10_users, get_user_leaderboard, get_user_position
from QQSM.states.login_state import LoginState


#Estado reflex de leaderboard_page que gestiona los datos que se usan para representar leaderboard_page

class LeaderboardState(LoginState):

    #Maxima puntuación del usuario loggeado
    max_score: int = 0
    #Estructura que almacena los top10 usuarios obtenidos de la base de datos
    top_users: list[tuple[str, int]] = []

    #Posición en el ranking global del usuario loggeado
    position: int = -1

    #Función que inicializa las variables anteriores realizando busquedas en la base de datos, se ejecuta cada vez que se carga leaderboard_page
    @rx.event
    def load(self):
        users = get_top_10_users() or []

        # Filtramos posibles filas con datos nulos
        self.top_users = [(i + 1, username, score) for i, (username, score) in enumerate(users)
                          if username is not None and score is not None]

        row = get_user_leaderboard(self.username)
        self.max_score = row[0][1] if row else -1
        self.position = get_user_position(self.username)
