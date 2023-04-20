from anime.factory import AnimesOnline
from animesonline.anime_release import AnimeReleaseDb
from animesonline.ep_release import EpisodeReleaseDb
from animesonline.production import SerieDb
from release.factory import AnimesonlineReleases
from website.interface import SiteInterface


class Animesonline(SiteInterface):
    def __init__(self, parser, requester) -> None:
        self.parser = parser
        self.requester = requester

    def get_anime(self, url):
        a = AnimesOnline().get_serie(url, self.parser, self.requester)
        return a

    def get_ep_releases(self):
        ep = AnimesonlineReleases(self.parser, self.requester)
        return ep.ep_releases()

    def get_anime_releases(self):
        ep = AnimesonlineReleases(self.parser, self.requester)
        return ep.anime_releases()

    @staticmethod
    def get_series_db(db_engine) -> SerieDb:
        se_db = SerieDb(db_engine)
        return se_db

    @staticmethod
    def get_ep_releases_db(db_engine):
        ep_db = EpisodeReleaseDb(db_engine)
        return ep_db

    @staticmethod
    def get_anime_releases_db(db_engine):
        anime_rel_db = AnimeReleaseDb(db_engine)
        return anime_rel_db
