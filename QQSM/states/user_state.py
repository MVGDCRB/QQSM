import reflex as rx
from QQSM.auth import get_user_full_stats
from QQSM.states.leaderboard_state import LeaderboardState

class UserState(LeaderboardState):
    tema_stats: list[str] = []

    @rx.event
    def load_user_data(self):
        data = get_user_full_stats(self.username)
        if data:
            self.max_score = data["max_score"]
            self.position = data["position"]
            self.tema_stats = data["tema_stats"]

