from anime.interfaces import SerieInterface, ProductionsDbInterface
from release.interfaces import ReleaseDbInterface
from website.interface import SiteInterface

import animesonline_online.anime_release
import animesonline_online.ep_releases
import  animesonline_online.production 

import anime.factory
import release.factory


class AnimesonlineOnline(SiteInterface):
    def __init__(self, parser, requester, db_engine) -> None:
        self.parser = parser
        self.requester = requester
        self.db_engine = db_engine

    def get_anime(self, url) -> SerieInterface:
        a = anime.factory.AnimesOnlineOnlineProduction()
        return a.get_serie(url, self.parser, self.requester)

    def get_ep_releases(self) -> list[dict[str, str | int | float]]:
        ep = release.factory.AnimesOnlineOnlineReleases(self.parser, 
                                                        self.requester)
        return ep.ep_releases()

    def get_anime_releases(self) -> list[dict[str, str | int | float]]:
        animes = release.factory.AnimesOnlineOnlineReleases(self.parser, 
                                                            self.requester)
        return animes.anime_releases()

    def get_series_db(self) -> ProductionsDbInterface:
        se_db = animesonline_online.production.SerieDb(self.db_engine)
        return se_db

    def get_ep_releases_db(self) -> ReleaseDbInterface:
        ep_db = animesonline_online.ep_releases.EpisodeReleaseDb(self.db_engine)
        return ep_db

    def get_anime_releases_db(self) -> ReleaseDbInterface:
        anime_db = animesonline_online.anime_release.AnimeReleaseDb(self.db_engine)
        return anime_db
