from enum import Enum
from pathlib import Path

from parser.factory import Parsers
from requester.factory import Requesters

from animesbr.site import AnimesBr
from animesonline.site import Animesonline
from animesonline_online.site import AnimesonlineOnline
from database import databases

parser = Parsers.use_bs4()
requester = Requesters.use_requests()
db_engine = databases.SQLite()

SITEACTIVE_FILE = Path('available_sites/.site-active').absolute()

class Sites(Enum):
    animesonline = Animesonline(parser, requester, db_engine)
    animesbr = AnimesBr(parser, requester, db_engine)
    animesonline_online = AnimesonlineOnline(parser, requester, db_engine)

    @staticmethod
    def set_site(site):
        try:
            sitename = Sites[site].name
        except KeyError:
            print('\033[31mSite inválido.\033[m')
        else:
            with open(SITEACTIVE_FILE, 'w', encoding='utf-8') as f:
                f.write(f'{sitename}')

    @staticmethod
    def site_active():
        with open(SITEACTIVE_FILE, 'r', encoding='utf-8') as f:
            site = f.read().replace('\n', '')
            return Sites[site].name
