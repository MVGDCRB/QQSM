#Este archivo contendrá la configuración de la base de datos

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from QQSM.models import Base


# URL de conexión a PostgreSQL 
DATABASE_URL = "postgresql://postgres:5555@localhost:5432/qqsm_db"

# Configuración de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear todas las tablas si no existen
def init_db():
    Base.metadata.create_all(bind=engine)

