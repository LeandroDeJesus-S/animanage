try:
    import os, sys
    
    sys.path.append(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')
        )
    )
except: pass

import re
from pprint import pprint

from release.interfaces import ReleaseScrapingInterface
from parser.interfaces import ParserInterface
from requester.interfaces import RequesterInterface
from release.interfaces import ReleaseDbInterface


class AnimeRelease(ReleaseScrapingInterface):
    def __init__(self, parser: ParserInterface, requester: RequesterInterface):
        super().__init__(parser, requester)
        self.parser = parser
        self.requester = requester
        
        self.pages = [
            'https://ww31.animesonline.online/em-lancamento/',
        ]
        self.num_pages = len(self.pages)
        
    def get_releases(self) -> list[dict[str, str | int | float]]:
        animes = []
        for page in self.pages:
            content = self.requester.get_content(page)
            anime_names = self.parser.select_all(
                content, 'div.wp-content div ul li', text=True
            )
            animes += [{'anime': a, 'rate': 0.0} for a in anime_names]

        return animes


class AnimeReleaseDb(ReleaseDbInterface):
    def __init__(self, db_engine):
        self.db = db_engine
        self.table = 'animesonline_online_anime_release'
        self.fields = ('anime', 'rate')
        
    def save_releases(self, releases: list[dict[str, str | int |float]]):
        for release in releases:
            self.db.insert(
                table=self.table,
                fields=self.fields,
                values=(*release.values(),)
            )
        
    def verify_if_exists(self, data: str, insensitive: bool = False, limit: int = 60) -> bool:
        result = self.db.select(
            table=self.table, where=self.fields[0],
            like=data, insensitive=insensitive, limit=limit
        )

        if not result:
            return False
            
        return True
