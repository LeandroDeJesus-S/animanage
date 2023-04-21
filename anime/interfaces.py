from abc import ABC, abstractmethod
from typing import List, Dict

from parser.interfaces import ParserInterface
from requester.interfaces import RequesterInterface
from database.interface import DatabaseInterface


class MovieInterface(ABC):
    @abstractmethod
    def __init__(self, link: str, parser: ParserInterface,
                 requesters: RequesterInterface) -> None:
        """
        Args:
            link (str): filme url
            parsers (obj parser): A parser object to visualize html content
            requesters (obj requester): A requester object to make requests 
        """
    
    @abstractmethod
    def get_evaluation_points(self) -> float:
        """Get and return the evaluation points from the movie.
        
        rType: int or float"""
    
    @abstractmethod
    def get_sinopse(self) -> str: 
        """get the sinopse of the movie.
        
        Returns:
            str: the sinopse of the movie."""
    
    @abstractmethod
    def get_category(self) -> List[str]:
        """Get and return the category of the movie.

        Returns:
            List[str]: all the categories founded
        """


class SerieInterface(MovieInterface):
    def __init__(self, link: str, parser: ParserInterface, 
                 requester: RequesterInterface) -> None:
        """
        Args:
            link (str): filme url
            parsers (obj parser): A parser object to visualize html content
            requesters (obj requester): A requester object to make requests 
            
        StaticArgs:
            last_season (int): the last season of the serie
            last_ep (int): the last episode of the serie
        """
        super().__init__(link, parser, requester)
        self.last_season: int
        self.last_ep: int
    
    @abstractmethod
    def get_links(self) -> Dict[int, Dict[int, str]]:
        """Return a dictionary with the links to each episode in
        the format {se: {ep: link}}

        rType: Dict[int, Dict[int, str]]
        """

    @abstractmethod
    def get_last_season(self) -> int:
        """get and set last season value"""

    @abstractmethod
    def get_last_ep(self) -> int:
        """get and set last ep value"""


class ProductionsDbInterface(ABC):
    @abstractmethod
    def __init__(self, db_engine: DatabaseInterface) -> None:
        """
        Args:
            db_engine (DatabaseInterface): engine to make database operations
        
        Instance attributes:
            table (str): table name to save data
            fields (tuple[str, ...]): table field names
        """
        self.db_engine: DatabaseInterface
        self.table: str
        self.fields: tuple[str, ...]
    
    @abstractmethod
    def save_production(self, data: list[dict[str, str | int | float]]):
        """save the productions data in database
        
        Args:
            data to save in database
        
        Obs:
            The data values should have the same order as the database fields.
        """
    
    @abstractmethod
    def verify_if_exists(self, data, insensitive: bool = False, limit: int = 60) -> bool:
        """verify if a data is in the database, if it's return True if not return False

        Args:
            data (str): data to verify
            insensitive (bool, optional): if True make query with insensitive 
            case compares. Defaults to False.
            limit (int, optional): limit of data to verify. Defaults to 60.

        Returns:
            bool: True if exists, False if not
        """

    @abstractmethod
    def get_link(self, name: str, insensitive: bool = False, limit: int = 60) -> str:
        """get data from database

        Args:
            name: production name to get the link
            insensitive (bool, optional): if True make query with insensitive
            case compares. Defaults to False.
            limit (int, optional): limit of data to verify. Defaults to 60.

        Returns:
            str: link founded by name
        """
    
    @abstractmethod
    def alter_name(self, name: str, new_name: str):
        """alter the name in database"""
