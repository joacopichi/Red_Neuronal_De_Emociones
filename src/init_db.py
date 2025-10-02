from db.database import db_singleton, Base
from db.orm_models import (
    EmotionResult,
    Correction,
)


def init_db():
    engine = db_singleton.engine
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada ✅")


if __name__ == "__main__":
    init_db()
