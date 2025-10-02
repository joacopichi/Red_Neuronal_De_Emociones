from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def add(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, id: int) -> Optional[T]:
        return self.db.query(self.model).get(id)

    def list(self, limit: int = 100) -> List[T]:
        return self.db.query(self.model).limit(limit).all()
