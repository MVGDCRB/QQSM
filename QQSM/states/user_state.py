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

            self.tema_stats = []
            for stat in data["tema_stats"]:
                parts = stat.split(";")
                tema, correctas, falladas, aciertos, fallos = parts

                total = str(int(correctas) + int(falladas))

                pct = int(aciertos)
                if pct < 50:
                    r = 255
                    g = int((pct / 50) * 255)
                    b = 0
                else:
                    r = int((1 - (pct - 50) / 50) * 255)
                    g = 255
                    b = 0
                color = f"rgb({r},{g},{b})"

                self.tema_stats.append(f"{tema};{correctas};{falladas};{aciertos};{fallos};{color};{total}")


