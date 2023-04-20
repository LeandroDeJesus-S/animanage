def animesbr_website_factory():
    global AnimesBr
    from website.interface import SiteWithMovieInterface
    
    from anime.factory import Animesbr
    from release.factory import AnimesbrReleases
    

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


animesbr_website_factory()
