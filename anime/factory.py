from abc import ABC, abstractmethod
import anime.products as products


class Factory(ABC):
    @staticmethod
    @abstractmethod
    def get_serie():
        """return a serie object"""
        pass
    
    @staticmethod
    @abstractmethod
    def get_movie():
        """return a movie object"""
        pass


class AnimesOnline(Factory):
    @staticmethod
    def get_serie(url, parser, requester):
        serie = products.AnimesonlineSerie(url, parser, requester)
        return serie
    
    @staticmethod
    def get_movie(url, parser, requester):
        movie = products.AnimesonlineMovie(url, parser, requester)
        return movie
