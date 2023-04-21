try:
    import os
    import sys
    
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..'
            )
        )
    )

except:
    pass

from release.interfaces import ReleaseScrapingInterface
from release.interfaces import ReleaseDbInterface
from parser.interfaces import ParserInterface
from requester.interfaces import RequesterInterface

class Animesflix(ReleaseScrapingInterface):
    def __init__(self, parser: ParserInterface, requester: RequesterInterface):
        super().__init__(parser, requester)
        self.parser = parser
        self.requester = requester
        
        self.pages = ['https://animesflix.net/']
        self.num_pages = len(self.pages)
    
    def get_releases(self) -> list[dict[str, str | int | float]]:  # type: ignore
        for page in self.pages:
            content = self.requester.get_content(page, type='text')
            
            titles = self.parser.select_all(
                content, 'header.entry-header h2.entry-title', text=True
            )
            eps = self.parser.select_all(
                content, 'header.entry-header span.num-epi', text=True
            )
            
            if titles is None or eps is None:
                return []
            
            titles = [t for t in titles if not t.startswith('\n')]
            releases = [{'title': f'{title} {ep}'} for title, ep in zip(titles, eps)]
            
            return releases  # type: ignore


class EpisodeReleaseDb(ReleaseDbInterface):
    def __init__(self, db_engine):
        self.db = db_engine
        self.table = 'animesflix_episode_release'
        self.fields = ('title',)
        
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