from abc import ABC, abstractmethod
from animesonline.production import AnimesonlineSerie
from animesbr.production import AnimesbrSerie


class FactoryMovie(ABC):
    @staticmethod
    @abstractmethod
    def get_movie(url: str, parser, requester):
        """return a movie object"""
        
class FactorySerie(ABC):
    @staticmethod
    @abstractmethod
    def get_serie(url: str, parser, requester):
        """return a serie object"""
        
class FactoryProduction(FactoryMovie, FactorySerie):
    @staticmethod
    @abstractmethod
    def get_serie(url: str, parser, requester):
        """return a serie object"""
        pass
    
    @staticmethod
    @abstractmethod
    def get_movie(url: str, parser, requester):
        """return a movie object"""
        pass


class AnimesOnline(FactorySerie):
    @staticmethod
    def get_serie(url, parser, requester):
        serie = AnimesonlineSerie(url, parser, requester)
        return serie


class Animesbr(FactorySerie):
    @staticmethod
    def get_serie(url, parser, requester):
        serie = AnimesbrSerie(url, parser, requester)
        return serie
