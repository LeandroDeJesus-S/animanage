from abc import ABC, abstractmethod
from typing import Tuple, List, Union, Any

T = Union[str, int, float]


class DatabaseInterface(ABC):
    connection = None
    cursor = None
    connected = None

    @classmethod
    @abstractmethod
    def connect(cls, db: str): pass

    @classmethod
    @abstractmethod
    def disconnect(cls): pass

    @classmethod
    @abstractmethod
    def insert(cls, table: str, fields: Tuple[str, ...], values: Tuple[T, ...]):
        pass

    @classmethod
    @abstractmethod
    def select(cls, table: str, limit: int=60, where: str='',
               like: str='', insensitive: bool=False) -> List[tuple]:
        pass

    @classmethod
    @abstractmethod
    def update(cls, table: str, setField: str,
               setValue: str, whereField: str, whereValue: str):
        pass

    @classmethod
    @abstractmethod
    def delete(cls, table: str, where: str, like: str):
        pass