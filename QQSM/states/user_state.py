import reflex as rx
from QQSM.auth import get_user_full_stats
from QQSM.states.leaderboard_state import LeaderboardState
from QQSM.styles.colors import Colors

#Reflex State de la página user_page, que gestiona los datos que se presentan en dicha página

class UserState(LeaderboardState):
    
    #Estructura que recoge las estadisticas por tema
    tema_stats: list[str] = []
    #Variable que almacena el numero de preguntas total respondido por el usuario
    total_questions: int = -1

    #Inicializa las estructuras anteriores con datos de la base de datos añadiendo un color a la puntuación obtenida por tema para su posterior representación

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

                porcentajeAciertos = int(aciertos)
                
                color = self.interpolate_color(porcentajeAciertos, Colors.FAILURE_RED, Colors.SUCCESS_GREEN)

                self.tema_stats.append(f"{tema};{correctas};{falladas};{aciertos};{fallos};{color};{total}")

        self.total_questions = sum(int(stat.split(';')[1]) + int(stat.split(';')[2]) for stat in self.tema_stats)

    #Pasa de string con color rgb a la tupla de enteros (r,g,b)
    def hex_to_rgb(self, hex_color: str) -> tuple[int, int, int]:
        hex_color = hex_color.lstrip("#")
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
    )

    #Interpola linealmente entre dos colores proporcionalmente al porcentaje de aciertos
    def interpolate_color(self, percentage:int, start_hex: str, end_hex: str) -> str:

        r0, g0, b0 = self.hex_to_rgb(start_hex)
        r1, g1, b1 = self.hex_to_rgb(end_hex)
        
        frac = max(0, min(percentage, 100)) / 100
        
        r = round(r0 + (r1 - r0) * frac)
        g = round(g0 + (g1 - g0) * frac)
        b = round(b0 + (b1 - b0) * frac)
        return f"rgb({r},{g},{b})"
