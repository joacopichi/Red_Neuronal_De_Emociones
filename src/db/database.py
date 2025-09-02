from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config import DATABASE_URL
import threading

Base = declarative_base()

class DatabaseSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_engine()
        return cls._instance

    def _init_engine(self):
        # future=True para SQLAlchemy moderno; echo=False para no spamear logs
        self.engine = create_engine(DATABASE_URL, echo=False, future=True)
        self.SessionLocal = scoped_session(sessionmaker(bind=self.engine, autoflush=False, autocommit=False))

    def get_session(self):
        return self.SessionLocal()

db_singleton = DatabaseSingleton()
