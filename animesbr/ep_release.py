from release.interfaces import ReleaseScrapingInterface

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'


# TODO: Move to animesbr own folder
class Animesbr(ReleaseScrapingInterface):
    def __init__(self, parser, requester):
        super().__init__(parser, requester)
        self.parser = parser
        self.requester = requester
        self.pages = [
            'https://animesbr.cc/episodio/',
            'https://animesbr.cc/episodio/page/2/',
        ]
        self.num_pages = len(self.pages)
        
    def get_releases(self) -> list[dict[str, str | int | float]]:
        releases = []
        for page in self.pages:
            content = self.requester.get_content(page, type='text', headers={'User-Agent': USER_AGENT})
            titles = self.parser.select_all(
                content, '.eptitle a', text=True
            )

            if titles is None:
                return [{}]
            
            releases.append([{'title': i} for i in titles])
            
        return releases
