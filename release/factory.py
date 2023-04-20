from abc import ABC, abstractmethod
import animesonline.ep_release, animesonline.anime_release
import animesbr.ep_release, animesbr.anime_release


class ReleaseFactory:
    @abstractmethod
    def __init__(self, parser, requester):
        """
        Args:
            parser (Parser): the parser to parser html content
            requester (Requester): the requester to get website content
        """
        self.parser = parser
        self.requester = requester
    
    @abstractmethod
    def ep_releases(self) -> list[dict[str, str | int | float]]:
        """return a list of episode releases in dict format"""
    
    @abstractmethod
    def anime_releases(self) -> list[dict[str, str | int | float]]:
        """return a list of anime releases in dict format"""

 
class AnimesonlineReleases(ReleaseFactory):
    def __init__(self, parser, requester):
        self.parser = parser
        self.requester = requester
        
    def ep_releases(self):
        eps = animesonline.ep_release.Animesonline(self.parser, self.requester)
        return eps.get_releases()
    
    def anime_releases(self):
        animes = animesonline.anime_release.AnimesOnline(self.parser, self.requester)
        return animes.get_releases()
 
 
class AnimesbrReleases(ReleaseFactory):
    def __init__(self, parser, requester):
        self.parser = parser
        self.requester = requester
        
    def ep_releases(self):
        eps = animesbr.ep_release.Animesbr(self.parser, self.requester)
        return eps.get_releases()
    
    def anime_releases(self):
        animes = animesbr.anime_release.AnimesBr(self.parser, self.requester)
        return animes.get_releases()
