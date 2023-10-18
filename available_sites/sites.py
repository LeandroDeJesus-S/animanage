from enum import Enum
import logging as log
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

SITEACTIVE_FILE = Path(__file__).parent.absolute() / '.site-active'
if not SITEACTIVE_FILE.exists():
    SITEACTIVE_FILE.touch()


class Sites(Enum):
    animesonline = Animesonline(parser, requester, db_engine)
    animesbr = AnimesBr(parser, requester, db_engine)
    animesonline_online = AnimesonlineOnline(parser, requester, db_engine)

    @staticmethod
    def set_site(site):
        try:
            sitename = Sites[site].name
            log.debug(f'sitename = {sitename}')
            
        except KeyError:
            print('\033[31mSite inválido.\033[m')
            
        else:
            with open(SITEACTIVE_FILE, 'w', encoding='utf-8') as f:
                f.write(f'{sitename}')
                log.debug(f'site registered')

    @staticmethod
    def site_active():
        with open(SITEACTIVE_FILE, 'r', encoding='utf-8') as f:
            site = f.read().replace('\n', '')
            log.debug(f'site = {site}')
            return Sites[site].name
