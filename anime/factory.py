from abc import ABC, abstractmethod

import animesonline.production
import animesbr.production
import animesonline_online.production


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


class AnimesOnlineProduction(FactorySerie):
    @staticmethod
    def get_serie(url, parser, requester):
        serie = animesonline.production.AnimesonlineSerie(url, parser, requester)
        return serie


class AnimesBrProduction(FactorySerie):
    @staticmethod
    def get_serie(url, parser, requester):
        serie = animesbr.production.AnimesbrSerie(url, parser, requester)
        return serie


class AnimesOnlineOnlineProduction(FactorySerie):
    @staticmethod
    def get_serie(url: str, parser, requester):
        serie = animesonline_online.production.AnimesonlineOnlineSerie(url, parser, requester)
        return serie
