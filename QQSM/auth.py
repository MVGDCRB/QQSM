# Funciones de registro y autenticación

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import desc
from db.models import User
from db.database import SessionLocal
from datetime import datetime

# Configuración para el hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from sqlalchemy import func

def get_user_position(username: str):
    return -1


def get_top_10_users():
    # # Obtén los 10 usuarios con la mayor puntuación
    db: Session = SessionLocal()
    try:
        # Realizar la consulta para obtener los 10 usuarios con mayor maxPuntuacion
        top_users = db.query(User.username, User.max_puntuacion).order_by(User.max_puntuacion.desc()).limit(10).all()
        db.close()
        return top_users  # Devuelve la lista de usuarios con mayor puntuación
    except Exception as e:
        print(f"Error al obtener los usuarios: {e}")
        db.close()
        return []

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
    if existing_user:
        raise Exception("El nombre de usuario ya está en uso")
        print("❌ Usuario registrado con éxito")

    
    # Crear el usuario
    hashed_password = get_password_hash(password)
    new_user = new_user = User(
        username=username, 
        password=hashed_password, 
        fecha_union=datetime.now(),  # Fecha de unión del usuario
        tema_stats={},  # Inicializamos las estadísticas de los temas vacías
        max_puntuacion=0
    )
    db.add(new_user)
    db.commit()
    db.close()


def login_user(username: str, password: str, db: Session) -> bool:
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
