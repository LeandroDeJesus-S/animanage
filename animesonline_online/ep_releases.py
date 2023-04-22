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


class EpisodeRelease(ReleaseScrapingInterface):
    def __init__(self, parser: ParserInterface, requester: RequesterInterface):
        super().__init__(parser, requester)
        self.parser = parser
        self.requester = requester
        
        self.pages = [
            'https://ww31.animesonline.online/episodios/',
            'https://ww31.animesonline.online/episodios/page/2/',
        ]
        self.num_pages = len(self.pages)
    
    def get_releases(self) -> list[dict[str, str | int | float]]:  # type: ignore
        data = []
        for page in self.pages:
            content = self.requester.get_content(page, type='text')
            
            titles = self.parser.select_all(
                content, 'div.eptitle a', text=True
            )

            data += [{'title': title} for title in titles]

        return data


class EpisodeReleaseDb(ReleaseDbInterface):
    def __init__(self, db_engine):
        self.db = db_engine
        self.table = 'animesonline_online_episode_release'
        self.fields = ('title',)
        
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
