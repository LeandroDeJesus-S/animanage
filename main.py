from parser.factory import Parsers
from requester.factory import Requesters
from website.interface import SiteInterface

from available_sites import sites

parser = Parsers.use_bs4()
requester = Requesters.use_requests()


class Cliente:
    def __init__(self):
        self.sites = sites.Sites
        self.site_active = sites.site_active()
        
        self.site: SiteInterface = self.sites[self.site_active].value
        self.site_ep_releases = self.site.get_ep_releases() 
        self.site_anime_releases = self.site.get_anime_releases() 
                
    def watch(self, anime, se=1, ep=1):
        # TODO: use a db operator to get the anime link by name
        link = 'https://animesonlinecc.to/anime/revenger/'
        
        anime = self.site.get_anime(link)
        links = anime.get_links()
        try:
            print(f'redirecting to: {links[se][ep]}')
        except KeyError:
            print('\033[31mTemporada ou episódio não encontrados.\033[m')
        

if __name__ == '__main__':
    pass
