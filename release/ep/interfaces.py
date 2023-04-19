from abc import ABC, abstractmethod

from parser.interfaces import ParserInterface
from requester.interfaces import RequesterInterface

class ReleaseScraping(ABC):
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
            with eps release
        """