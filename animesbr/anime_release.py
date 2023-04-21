import re

from release.interfaces import ReleaseScrapingInterface
from parser.interfaces import ParserInterface
from requester.interfaces import RequesterInterface
from release.interfaces import ReleaseDbInterface


class AnimesBr(ReleaseScrapingInterface):
    def __init__(self, parser: ParserInterface, requester: RequesterInterface):
        super().__init__(parser, requester)
        self.parser = parser
        self.requester = requester
        
        self.pages = [
            'https://animesbr.cc/anime/',
            'https://animesbr.cc/anime/page/2/',
        ]
        self.num_pages = len(self.pages)
        
    def get_releases(self) -> list[dict[str, str | int | float]]:
        animes, rates = [], []
        for page in self.pages:
            content = self.requester.get_content(page)
            anime_names = self.parser.select_all(
                content, 'div.data h3 a', text=True
            )
            anime_rates = self.parser.select_all(
                content, 'div.rating', text=True
            )
            
            if anime_names is None or anime_rates is None:
                continue
            
            for rate in anime_rates:
                if not rate:
                    rates.append(0.0)
                    continue
                
                rate = float(re.sub(r'[^\d.]', ' ', rate).split()[0])
                rates.append(rate)
                
            animes.extend(anime_names)
    
        final_animes = []
        for a, r in zip(animes, rates):
            final_animes.append({'anime': a, 'rate': r})

        return final_animes


class AnimeReleaseDb(ReleaseDbInterface):
    def __init__(self, db_engine):
        self.db = db_engine
        self.table = 'animesbr_anime_release'
        self.fields = ('anime', 'rate')
        
    def save_releases(self, releases: list[dict[str, str | int |float]]) -> bool:
        try:
            for release in releases:
                self.db.insert(
                    table=self.table, 
                    fields=self.fields, 
                    values=(*release.values(),)
                )
            return True
        
        except Exception as error:
            return False
        
    def verify_if_exists(self, data: str, insensitive: bool = False, limit: int = 60) -> bool:
        result = self.db.select(
            table=self.table, where=self.fields[0],
            like=data, insensitive=insensitive, limit=limit
        )

        if not result:
            return False
            
        return True