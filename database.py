from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a PostgreSQL (ajusta con tus credenciales)
DATABASE_URL = "postgresql://taller_db_x0h8_user:n4Bj2iFgT8NmMUhxTOMScLRoLvpwMEsL@dpg-cv86n8rqf0us73f682a0-a/taller_db_x0h8"

# Configurar la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
