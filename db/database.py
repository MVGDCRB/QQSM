# Este archivo contendrá la configuración de la base de datos

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base


DB_USER = "postgres"
DB_PASSWORD = "5555"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "qqsm_db"

#Url de la base de datos parametrizada
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Configuración de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Creación de la base de datos
def init_db():
    Base.metadata.create_all(bind=engine)
