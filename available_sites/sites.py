from enum import Enum
from typing import Literal

from parser.factory import Parsers
from requester.factory import Requesters
from website.interface import SiteInterface

from animesbr import animesbr
from animesonline import animesonline
from animesbr.animesbr import AnimesBr

parser = Parsers.use_bs4()
requester = Requesters.use_requests()


class Sites(Enum):
    animesonline = animesonline.Animesonline(parser, requester)
    animesbr = animesbr.AnimesBr(parser, requester)
    
    
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
