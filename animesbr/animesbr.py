def animesbr_website_factory():
    global AnimesBr
    from website.interface import SiteWithMovieInterface
    
    from anime.factory import Animesbr
    from release.factory import AnimesbrReleases
    from animesbr.production import SerieDb
    from animesbr.anime_release import AnimeReleaseDb
    from animesbr.ep_release import EpisodeReleaseDb

    class AnimesBr(SiteWithMovieInterface):
        def __init__(self, parser, requester) -> None:
            self.parser = parser
            self.requester = requester
            
        def get_anime(self, url):
            a = Animesbr().get_serie(url, self.parser, self.requester)
            return a
        
        def get_movie(self, url):
            raise NotImplementedError('Not Implemented yet')
        
        def get_ep_releases(self):
            ep = AnimesbrReleases(self.parser, self.requester)
            return ep.ep_releases()
        
        def get_anime_releases(self):
            ep = AnimesbrReleases(self.parser, self.requester)
            return ep.anime_releases()

        def get_serie_db(self, db_engine):
            db = SerieDb(db_engine)
            return db
        
        def get_ep_releases_db(self, db_engine):
            ep_db = EpisodeReleaseDb(db_engine)
            return ep_db
        
        def get_anime_releases_db(self, db_engine):
            anime_rel_db = AnimeReleaseDb(db_engine)
            return anime_rel_db
        

animesbr_website_factory()
