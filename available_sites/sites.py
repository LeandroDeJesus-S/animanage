from enum import Enum

from parser.factory import Parsers
from requester.factory import Requesters

from animesonline.site import Animesonline
from animesbr.site import AnimesBr

parser = Parsers.use_bs4()
requester = Requesters.use_requests()


class Sites(Enum):
    animesonline = Animesonline(parser, requester)
    animesbr = AnimesBr(parser, requester)
    
    
def show_sites():
    for s in Sites:
        print(s.name)
        

def set_site(site):
    try:
        sitename = Sites[site].name
    except KeyError:
        print('\033[31mSite não disponível\033[m')
    else:
        with open('available_sites/.site-active', 'w', encoding='utf-8') as f:
            f.write(f'{sitename}')


def site_active():
    with open('available_sites/.site-active', 'r', encoding='utf-8') as f:
        site = f.read().replace('\n', '')
        return Sites[site].name
