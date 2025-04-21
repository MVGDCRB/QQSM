from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.models import User
from db.database import SessionLocal
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_position(username: str) -> int:
    """Devuelve la posición global del usuario según: puntuación DESC, orden de inserción."""
    db = SessionLocal()
    try:
        ordered_users = (
            db.query(User.username, User.max_puntuacion)
            .order_by(User.max_puntuacion.desc(), User.id.asc())# desempate por orden de inserción
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
    # Verificar si el nombre de usuario ya existe
    existing_user = db.query(User).filter(User.username == username).first()

    if not existing_user:
        # Crear el usuario
        hashed_password = get_password_hash(password)
        new_user = User(
            username=username,
            password=hashed_password,
            fecha_union=datetime.now(),  # Fecha de unión del usuario
            tema_stats={},  # Inicializamos las estadísticas de los temas vacías
            max_puntuacion=0
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


def current_user():
    """Por ahora, simplemente devuelve un nombre de usuario estático para pruebas."""
    return "test_user"
