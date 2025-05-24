from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Configuración de la base de datos SQLAlchemy
Base = declarative_base()


class User(Base):
    """Modelo de tabla de usuarios."""
    __tablename__ = "users"
    
    #Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)
    #Nombre de usuario
    username = Column(String(50), nullable=False, unique=True)
    #Contraseña
    password = Column(String(128), nullable=False)
    #Fecha de unión a la aplicación
    fecha_union = Column(DateTime, default=datetime.now)
    #Estadísticas por temas
    tema_stats = Column(JSON, default={})
    #Máxima puntuación alcanzada
    max_puntuacion = Column(Integer, default=0, nullable=False)
    
    #representación textual de fila User
    def __repr__(self):
        return f"<User(username={self.username})>"
