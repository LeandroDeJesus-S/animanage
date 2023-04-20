from release.interfaces import ReleaseScrapingInterface, ReleaseDbInterface

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'


class Animesonline(ReleaseScrapingInterface):
    def __init__(self, parser, requester):
        super().__init__(parser, requester)
        self.parser = parser
        self.requester = requester
        self.pages = [
            'https://animesonlinecc.to/episodio/',
            'https://animesonlinecc.to/episodio/page/2/',
        ]
        self.num_pages = len(self.pages)
        
    def get_releases(self) -> list[dict[str, str | int | float]]:
        releases = []
        for page in self.pages:
            content = self.requester.get_content(page, type='text', headers={'User-Agent': USER_AGENT})
            titles = self.parser.select_all(
                content, '.eptitle', text=True, features='html.parser'
            )

            if titles is None:
                return [{}]
            
            releases += [{'title': i} for i in titles]
            
        return releases
    

class EpisodeReleaseDb(ReleaseDbInterface):
    def __init__(self, db_engine):
        self.db = db_engine
        self.table = 'animesonline_episode_release'
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
