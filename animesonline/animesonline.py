def animesonline_website_factory():
    global Animesonline
    from website.interface import SiteInterface
    
    from anime.factory import AnimesOnline
    from release.factory import AnimesonlineReleases
    

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


animesonline_website_factory()
