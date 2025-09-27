from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

DATABASE_URL = "sqlite:///./src/red_emociones.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function para FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """
    Inicializa la base de datos creando todas las tablas
    """
    Base.metadata.create_all(bind=engine)

class Database:
    def __init__(self):
        self._engine = engine
        self._SessionLocal = SessionLocal

    def get_session(self) -> Session:
        """
        Retorna una sesión de base de datos (para servicios)
        """
        return self._SessionLocal()

db_singleton = Database()
