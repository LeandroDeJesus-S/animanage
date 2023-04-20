import re

from release.interfaces import ReleaseScrapingInterface
from parser.interfaces import ParserInterface
from requester.interfaces import RequesterInterface


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