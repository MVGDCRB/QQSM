from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.models import User
from db.database import SessionLocal
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def update_max_score(username: str, score: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and score > user.max_puntuacion:
            user.max_puntuacion = score
            db.commit()
    finally:
        db.close()


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


def get_user_full_stats(username: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            if not user.tema_stats or not isinstance(user.tema_stats, dict) or len(user.tema_stats) < 15:
                default_stats = {
                    tema: {"correctas": 0, "falladas": 0}
                    for tema in [
                        "arte", "fisica", "historia", "quimica", "musica", "matematicas",
                        "literatura", "biologia", "historia de la television", "videojuegos",
                        "moda", "tecnologia", "cocina", "deportes", "geografia"
                    ]
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


def get_user_position(username: str) -> int:
    """Devuelve la posición global del usuario según: puntuación DESC, orden de inserción."""
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


def get_user_leaderboard(username: str):
    db: Session = SessionLocal()
    try:
        # Realizar la consulta para obtener el usuario y la puntuacion
        user = db.query(User.username, User.max_puntuacion).filter(User.username == username).all()
        db.close()
        return user  # Devuelve la lista de usuarios con mayor puntuación
    except Exception as e:
        print(f"Error al obtener el usuario: {e}")
        db.close()
        return []


def get_password_hash(password: str) -> str:
    """Genera un hash de la contraseña."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica la contraseña."""
    return pwd_context.verify(plain_password, hashed_password)


def create_user(username: str, password: str, db: Session):
    existing_user = db.query(User).filter(User.username == username).first()

    if not existing_user:
        hashed_password = get_password_hash(password)
        
        tema_stats_default = {
            tema: {"correctas": 0, "falladas": 0}
            for tema in [
                "arte", "fisica", "historia", "quimica", "musica", "matematicas",
                "literatura", "biologia", "historia de la television", "videojuegos",
                "moda", "tecnologia", "cocina", "deportes", "geografia"
            ]
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


def login_user(username: str, password: str) -> bool:
    """Verifica si el usuario puede iniciar sesión."""
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if user and verify_password(password, user.password):
        return True
    else:
        return False

