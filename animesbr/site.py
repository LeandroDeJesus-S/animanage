
from anime.interfaces import SerieInterface, ProductionsDbInterface
from release.interfaces import ReleaseDbInterface
from website.interface import SiteWithMovieInterface

import animesbr.anime_release
import animesbr.ep_release
import animesbr.production

import anime.factory
import release.factory


class AnimesBr(SiteWithMovieInterface):
    def __init__(self, parser, requester, db_engine) -> None:
        self.parser = parser
        self.requester = requester
        self.db_engine = db_engine

    def get_anime(self, url) -> SerieInterface:
        a = anime.factory.AnimesBrProduction()
        return a.get_serie(url, self.parser, self.requester)

    def get_movie(self, url):
        raise NotImplementedError('Not Implemented yet')

    def get_ep_releases(self) -> list[dict[str, str | int | float]]:
        ep = release.factory.AnimesbrReleases(self.parser, self.requester)
        return ep.ep_releases()

    def get_anime_releases(self) -> list[dict[str, str | int | float]]:
        ep = release.factory.AnimesbrReleases(self.parser, self.requester)
        return ep.anime_releases()

    def get_series_db(self) -> ProductionsDbInterface:
        db = animesbr.production.SerieDb(self.db_engine)
        return db

    def get_ep_releases_db(self) -> ReleaseDbInterface:
        ep_db = animesbr.ep_release.EpisodeReleaseDb(self.db_engine)
        return ep_db

    def get_anime_releases_db(self) -> ReleaseDbInterface:
        anime_rel_db = animesbr.anime_release.AnimeReleaseDb(self.db_engine)
        return anime_rel_db
