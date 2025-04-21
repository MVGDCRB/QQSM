from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Configuración de la base de datos SQLAlchemy
Base = declarative_base()


class User(Base):
    """Modelo de tabla de usuarios."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    fecha_union = Column(DateTime, default=datetime.now)  # Nuevo campo para la fecha de unión
    tema_stats = Column(JSON, default={})  # Nuevo campo para las estadísticas de los temas
    max_puntuacion = Column(Integer, default=0, nullable=False)
    

    def __repr__(self):
        return f"<User(username={self.username})>"
