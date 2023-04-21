from abc import ABC, abstractmethod
from anime.interfaces import SerieInterface, MovieInterface, ProductionsDbInterface
from release.interfaces import ReleaseScrapingInterface, ReleaseDbInterface



class SiteInterface(ABC):
    @abstractmethod
    def __init__(self, parser, requester) -> None:
        self.parser = parser
        self.requester = requester

        self.table: str
        self.fields: tuple[str, ...]
        
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

    @staticmethod
    @abstractmethod
    def get_series_db(db_engine) -> ProductionsDbInterface:
        """return series database object"""

    @staticmethod
    @abstractmethod
    def get_ep_releases_db(db_engine) -> ReleaseDbInterface:
        """return ep release database object"""

    @staticmethod
    @abstractmethod
    def get_anime_releases_db(db_engine) -> ReleaseDbInterface:
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