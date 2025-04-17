import reflex as rx
from QQSM.auth import get_top_10_users, get_user_leaderboard,get_user_position

class LeaderboardState(rx.State):
    max_score: int = 0
    top_users: list[tuple[str, int]] = []
    position:   int = -1

    @rx.event              
    def load(self, username: str = ""):
        """Rellena ranking y puntuación del usuario indicado."""
        if not username:          # si aún no hay sesión, nada que hacer
            return

        self.top_users = get_top_10_users()
        row = get_user_leaderboard(username)
        self.max_score = row[0][1] if row else -1
        self.position = get_user_position(username)

