from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.models import User
from db.database import SessionLocal
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Posibles temáticas de las preguntas
topics = ["arte", "fisica", "historia", "quimica", "musica", "matematicas",
        "literatura", "biologia", "historia de la television", "videojuegos",
        "moda", "tecnologia", "cocina", "deportes", "geografia"]

#Función que actualiza la puntuación máxima del usuario en la base de datos, usando la puntuación actual del usuario
def update_max_score(username: str, score: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and score > user.max_puntuacion:
            user.max_puntuacion = score
            db.commit()
    finally:
        db.close()

#Función que actualiza las estadísticas de aciertos del usuario en la base de datos, usando el tema de la pregunta respondida por el usuario
def update_user_stats(username: str, tema: str, acierto: bool):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return

        if tema not in user.tema_stats:
            user.tema_stats[tema] = {"correctas": 0, "falladas": 0}

        if acierto:
            user.tema_stats[tema]["correctas"] += 1
        else:
            user.tema_stats[tema]["falladas"] += 1

        flag_modified(user, "tema_stats")  # Actualiza la base de datos
        db.commit()
    finally:
        db.close()

#Función que recoge las estadísticas actuales del usuario de la base de datos para ser mostradas en el perfil
def get_user_full_stats(username: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            if not user.tema_stats or not isinstance(user.tema_stats, dict) or len(user.tema_stats) < 15:
                default_stats = {
                    tema: {"correctas": 0, "falladas": 0}
                    for tema in topics
                }
                user.tema_stats = default_stats
                db.commit() 

            lista_stats = []
            for tema, stats in user.tema_stats.items():
                c = stats["correctas"]
                f = stats["falladas"]
                total = c + f if c + f > 0 else 1
                acierto_pct = round(c / total * 100)
                fallo_pct = round(f / total * 100)
                lista_stats.append(f"{tema};{c};{f};{acierto_pct};{fallo_pct}")

            return {
                "max_score": user.max_puntuacion,
                "position": get_user_position(username),
                "tema_stats": lista_stats
            }
        return {}
    finally:
        db.close()

#Función que devuelve la posición del usuario según su puntuación máxima en el ranking global.
def get_user_position(username: str) -> int:
    db = SessionLocal()
    try:
        ordered_users = (
            db.query(User.username, User.max_puntuacion)
            .order_by(User.max_puntuacion.desc(), User.id.asc())  # desempate por orden de inserción
            .all()
        )
        for idx, (uname, _) in enumerate(ordered_users, start=1):
            if uname == username:
                return idx
        return -1
    except Exception as e:
        print(f"Error al calcular posición: {e}")
        return -1
    finally:
        db.close()

#Función que devuelve la información de los primeros 10 usuarios del ranking global
def get_top_10_users():
    db: Session = SessionLocal()
    try:
        top_users = (
            db.query(User.username, User.max_puntuacion)
            .order_by(User.max_puntuacion.desc(), User.id.asc())  # desempate por orden de inserción
            .limit(10)
            .all()
        )
        return top_users
    except Exception as e:
        print(f"Error al obtener los usuarios: {e}")
        return []
    finally:
        db.close()

#Función que devuelve el nombre y la puntuación máxima de un usuario dado
def get_user_leaderboard(username: str):
    db: Session = SessionLocal()
    try:
        user = db.query(User.username, User.max_puntuacion).filter(User.username == username).all()
        db.close()
        return user
    except Exception as e:
        print(f"Error al obtener el usuario: {e}")
        db.close()
        return []

#Función que genera un hash para la contraseña de un usuario
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

#Función que verifica la contraseña de un usuario usando el hash guardado de dicha contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#Función que inicializa un nuevo usuario con nombre y contraseña y lo agrega a la base de datos
def create_user(username: str, password: str, db: Session):
    existing_user = db.query(User).filter(User.username == username).first()

    if not existing_user:
        hashed_password = get_password_hash(password)
        
        tema_stats_default = {
            tema: {"correctas": 0, "falladas": 0}
            for tema in topics

        }

        new_user = User(
            username=username,
            password=hashed_password,
            fecha_union=datetime.now(),
            max_puntuacion=0,
            tema_stats=tema_stats_default
        )

        db.add(new_user)
        db.commit()
        db.close()
    else:
        db.close()
        raise Exception("El nombre de usuario ya está en uso")

#Función que verifica que el login de un usuario tiene los parámetros correctos
def login_user(username: str, password: str) -> bool:
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if user and verify_password(password, user.password):
        return True
    else:
        return False

