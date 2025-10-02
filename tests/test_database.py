from src.db.database import get_db

def test_database_connection():
    db = get_db()
    assert db is not None