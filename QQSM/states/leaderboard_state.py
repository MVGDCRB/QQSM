import reflex as rx
from QQSM.auth import get_top_10_users, get_user_leaderboard, get_user_position
from QQSM.states.login_state import LoginState


class LeaderboardState(LoginState):
    """
    Estado que gestiona la información para la página de la tabla de clasificación (leaderboard).
    Hereda de LoginState para mantener la información de autenticación del usuario.
    """
    max_score: int = 0
    top_users: list[tuple[str, int]] = []
    position: int = -1

    @rx.event
    def load(self):
        users = get_top_10_users() or []

        # Filtramos posibles filas malformadas
        self.top_users = [(i + 1, username, score) for i, (username, score) in enumerate(users)
                          if username is not None and score is not None]

        row = get_user_leaderboard(self.username)
        self.max_score = row[0][1] if row else -1
        self.position = get_user_position(self.username)
