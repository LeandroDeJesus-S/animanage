from anime.factory import AnimesOnlineOnline
from animesonline_online.anime_release import AnimeReleaseDb
from animesonline_online.ep_releases import EpisodeReleaseDb
from animesonline_online.production import SerieDb
from release.factory import AnimesOnlineOnlineReleases
from website.interface import SiteInterface
from anime.interfaces import SerieInterface


class AnimesonlineOnline(SiteInterface):
    def __init__(self, parser, requester) -> None:
        self.parser = parser
        self.requester = requester

    def get_anime(self, url) -> SerieInterface:
        a = AnimesOnlineOnline().get_serie(url, self.parser, self.requester)
        return a

    def get_ep_releases(self):
        ep = AnimesOnlineOnlineReleases(self.parser, self.requester)
        return ep.ep_releases()

    def get_anime_releases(self):
        ep = AnimesOnlineOnlineReleases(self.parser, self.requester)
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
