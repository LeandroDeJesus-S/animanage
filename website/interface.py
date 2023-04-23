from abc import ABC, abstractmethod
from anime.interfaces import SerieInterface, MovieInterface, ProductionsDbInterface
from release.interfaces import ReleaseScrapingInterface, ReleaseDbInterface
from database.interface import DatabaseInterface
from parser.interfaces import ParserInterface
from requester.interfaces import RequesterInterface

class SiteInterface(ABC):
    @abstractmethod
    def __init__(
            self, parser: ParserInterface, 
            requester: RequesterInterface, 
            db_engine: DatabaseInterface
        ) -> None:
        
        self.parser = parser
        self.requester = requester
        self.db_engine = db_engine
        
    @abstractmethod
    def get_anime(self, url: str) -> SerieInterface:
        """return an anime object with their info

        Args:
            url (str): url of the anime

        Returns:
            Serie: Class of anime with methods to get information
        """
    
    @abstractmethod
    def get_ep_releases(self) -> list[dict[str, str | int | float]]:
        """return list of eps releases in a dictionary format"""
    
    @abstractmethod
    def get_anime_releases(self) -> list[dict[str, str | int | float]]:
        """return list of anime releases in a dictionary format"""

    @abstractmethod
    def get_series_db(self) -> ProductionsDbInterface:
        """return series database object"""

    @abstractmethod
    def get_ep_releases_db(self) -> ReleaseDbInterface:
        """return ep release database object"""

    @abstractmethod
    def get_anime_releases_db(self) -> ReleaseDbInterface:
        """return an anime release database object"""

    
class SiteWithMovieInterface(SiteInterface):
    @abstractmethod
    def get_movie(self, url: str) -> MovieInterface:
        """return a movie object with their info

        Args:
            url (str): url of the anime

        Returns:
            Movie: Class of anime with methods to get information
        """