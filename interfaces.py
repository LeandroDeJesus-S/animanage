from abc import ABC, abstractmethod
from typing import List, Dict


class MovieInterface(ABC):
    @abstractmethod
    def __init__(self, link: str, parsers, requesters) -> None:
        """
        Args:
            link (str): filme url
            parsers (obj parser): A parser object to visualize html content
            requesters (obj requester): A requester object to make requests 
        """
        self.link: str = link
    
    @abstractmethod
    def get_evaluation_points(self) -> float:
        """Get and return the evaluation points from the movie.
        
        rType: int or float"""
        pass
    
    @abstractmethod
    def get_sinopse(self) -> str: 
        """get the sinopse of the movie.
        
        Returns:
            str: the sinopse of the movie."""
        pass
    
    @abstractmethod
    def get_category(self) -> List[str]:
        """Get and return the category of the movie.

        Returns:
            List[str]: all the categories founded
        """
        pass


class SerieInterface(MovieInterface):
    def __init__(self, link: str, parsers, requesters) -> None:
        """
        Args:
            link (str): filme url
            parsers (obj parser): A parser object to visualize html content
            requesters (obj requester): A requester object to make requests 
            
        StaticArgs:
            last_season (int): the last season of the serie
            last_ep (int): the last episode of the serie
        """
        super().__init__(link, parsers, requesters)
        self.last_season: int
        self.last_ep: int
    
    @abstractmethod
    def get_links(self) -> Dict[int, Dict[int, str]]:
        """Return a dictionary with the links to each episode in
        the format {se: {ep: link}}

        rType: Dict[int, Dict[int, str]]
        """
        pass
