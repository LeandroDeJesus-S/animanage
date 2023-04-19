from time import sleep
from release.ep.interfaces import ReleaseScraping

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

class Animesonline(ReleaseScraping):
    def __init__(self, parser, requester):
        super().__init__(parser, requester)
        self.parser = parser
        self.requester = requester
        self.pages = [
            'https://animesbr.cc/episodio/'
            'https://animesonlinecc.to/episodio/page/2/'
            'https://animesonlinecc.to/episodio/page/3/'
        ]
        self.num_pages = len(self.pages)
        
    def get_releases(self) -> list[dict[str, str | int | float]]:
        releases = []
        for page in self.pages:
            sleep(.3)
            content = self.requester.get_content(page, type='text', headers={'User-Agent': USER_AGENT})
            titles = self.parser.select_all(
                content, '.content', text=True
            )

            if titles is None:
                return [{}]
            
            releases.append([{'title': i} for i in titles])
            
        return releases
    