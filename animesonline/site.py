from anime.interfaces import SerieInterface, ProductionsDbInterface
from release.interfaces import ReleaseDbInterface
from website.interface import SiteInterface

import animesonline.anime_release
import animesonline.ep_release
import  animesonline.production 

import anime.factory
import release.factory


class Animesonline(SiteInterface):
    def __init__(self, parser, requester, db_engine) -> None:
        self.parser = parser
        self.requester = requester
        self.db_engine = db_engine

    def get_anime(self, url) -> SerieInterface:
        a = anime.factory.AnimesOnlineProduction()
        return a.get_serie(url, self.parser, self.requester)

    def get_ep_releases(self) -> list[dict[str, str | int | float]]:
        eps = release.factory.AnimesonlineReleases(self.parser, self.requester)
        return eps.ep_releases()

    def get_anime_releases(self) -> list[dict[str, str | int | float]]:
        animes = release.factory.AnimesonlineReleases(self.parser, 
                                                      self.requester)
        return animes.anime_releases()

    def get_series_db(self) -> ProductionsDbInterface:
        se_db = animesonline.production.SerieDb(self.db_engine)
        return se_db

    def get_ep_releases_db(self) -> ReleaseDbInterface:
        ep_db = animesonline.ep_release.EpisodeReleaseDb(self.db_engine)
        return ep_db

    def get_anime_releases_db(self) -> ReleaseDbInterface:
        anime_rel_db = animesonline.anime_release.AnimeReleaseDb(self.db_engine)
        return anime_rel_db
