import reflex as rx
from QQSM.auth import get_top_10_users, get_user_leaderboard
from QQSM.states.login_state import LoginState

class LeaderboardState(rx.State):
    max_score: int = 0
    top_users: list[tuple[str, int]] = []

    @rx.event
    async def load(self):
        # ② pásale la clase, no un string
        login_state = await self.get_state(LoginState)
        username    = login_state.username
        if not username:
            return

        self.top_users = get_top_10_users()
        row = get_user_leaderboard(username)
        self.max_score = row[0][1] if row else 0
