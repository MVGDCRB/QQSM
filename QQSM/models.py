#este archivo contendrá las tablas de usuarios

from sqlalchemy import Column, String, Integer, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Configuración de la base de datos SQLAlchemy
Base = declarative_base()

class User(Base):
    """Modelo de tabla de usuarios."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    def __repr__(self):
        return f"<User(username={self.username})>"
