from abc import ABC, abstractmethod
from typing import Tuple, List, Union, Any

T = Union[str, int, float]


class DatabaseInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        """Instance Attrs:
            connection: receives the database connection 
            cursor: the cursor object to make operations
        """
        self.connection: Any
        self.cursor: Any
        
    @abstractmethod
    def connect(self, db: str): pass
    
    @abstractmethod
    def disconnect(self): pass

    @abstractmethod
    def insert(self, table: str, fields: Tuple[str, ...], values: Tuple[T, ...]):
        pass
    
    @abstractmethod
    def select(self, table: str, limit: int=60, where: str='', 
               like: str='', insensitive: bool=False) -> List[tuple]:
        pass
    
    @abstractmethod
    def update(self, table: str, setField: str, 
               setValue: str, whereField: str, whereValue: str):
        pass
    
    @abstractmethod
    def delete(self, table: str, where: str, like: str):
        pass