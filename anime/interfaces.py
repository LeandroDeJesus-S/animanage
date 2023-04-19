from abc import ABC, abstractmethod
from typing import List, Dict
from parser.interfaces import ParserInterface
from requester.interfaces import RequesterInterface

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
