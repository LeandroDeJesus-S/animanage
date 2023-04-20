from abc import ABC, abstractmethod

from parser.interfaces import ParserInterface
from requester.interfaces import RequesterInterface
from database.interface import DatabaseInterface

class ReleaseScrapingInterface(ABC):
    @abstractmethod
    def __init__(self, parser: ParserInterface, requester: RequesterInterface):
        """
        Instance Args:
            pages (list[str]): list of pages from eps to scraping data
            num_pages (int): number of pages that will be used
        """
        
    @abstractmethod
    def get_releases(self) -> list[dict[str, str | int | float]]:
        """get release data
        
        Returns:
            list[dict[str, str | int | float]]: list of dictionaries
            with release data
        """


class ReleaseDbInterface(ABC):
    @abstractmethod
    def __init__(self, db_engine: DatabaseInterface):
        """
        Args:
            db_engine (DatabaseInterface): database engine to make operations
        
        Local Args:
            table (str): table of animes release
            fields (tuple[str, ...]): fields of animes release table
        """
        self.table: str
        self.fields: tuple[str, ...]
        self.db = db_engine
        
    @abstractmethod
    def save_releases(self, releases: list[dict[str, str | int | float]]):
        """save release data into database

        Args:
            releases (list[dict[str, str  |  int  |  float]]): data to save
            
        Obs:
            The data values should have the same order as the database fields.
        """
    
    @abstractmethod
    def verify_if_exists(self, anime, insensitive: bool = False, limit: int = 60) -> bool: 
        """verify if an data is in the database, if it's return True if not return False

        Args:
            data (str): data to verify
            insensitive (bool, optional): if True make query with insensitive 
            case compares. Defaults to False.
            limit (int, optional): limit of data to verify. Defaults to 60.

        Returns:
            bool: True if exists, False if not
        """
