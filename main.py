from parser.factory import Parsers
from requester.factory import Requesters
from database.databases import SQLite
from anime.interfaces import ProductionsDbInterface
from website.interface import SiteInterface

from available_sites import sites

parser = Parsers.use_bs4()
requester = Requesters.use_requests()


class Client:
    def __init__(self):
        self.sites = sites.Sites
        self.site_active = sites.site_active()

        self.db_engine = SQLite()
        self.database = 'db.sqlite'

        self.site: SiteInterface = self.sites[self.site_active].value
        self.site_anime_db: ProductionsDbInterface = self.site.get_series_db(self.db_engine)
        self.site_ep_release_db = self.site.get_ep_releases_db(self.db_engine)
        self.site_anime_release_db = self.site.get_anime_releases_db(self.db_engine)
                
    def watch(self, anime, se=1, ep=1):
        # self.db_engine.select(self.site_db.table, where=self.db)
        self.db_engine.connect(self.database)
        link = self.site_anime_db.get_link(anime, insensitive=False)
        self.db_engine.disconnect()
        if not link:
            print('\033[31mNenhum resultado encontrado.\033[m')
            return

        anime = self.site.get_anime(link)
        links = anime.get_links()
        try:
            print(f'redirecting to: {links[se][ep]}')
        except KeyError:
            print('\033[31mTemporada ou episódio não encontrados.\033[m')

    def list_ep_release(self):
        try:
            releases = self.site.get_ep_releases()
            self.db_engine.connect(self.database)
            for release in releases:
                title = str(*release.values()).strip()
                if self.site_ep_release_db.verify_if_exists(title):
                    print(title)
                    continue

                print(f'\033[32m{title}\033[m')

            self.site_ep_release_db.save_releases(releases)
        finally:
            self.db_engine.disconnect()

    def list_anime_release(self):
        try:
            releases = self.site.get_anime_releases()
            self.db_engine.connect(self.database)
            for anime in releases:
                name, rate = anime.values()
                if not self.site_anime_release_db.verify_if_exists(name):
                    name = f'\033[32m{name}\033[m'

                print(name, self.colorize_rate(rate))

            self.site_anime_release_db.save_releases(releases)
        finally:
            self.db_engine.disconnect()

    @staticmethod
    def colorize_rate(rate: float) -> str:
        if rate < 5:
            rate = f'\033[31m{rate}'
        elif rate < 7:
            rate = f'\033[33m{rate}'
        elif rate < 9:
            rate = f'\033[32m{rate}'
        else:
            rate = f'\033[35m{rate}'
        return rate + '\033[m'

    def watch_latest(self, anime):
        self.db_engine.connect(self.database)
        link = self.site_anime_db.get_link(anime)
        anime = self.site.get_anime(link)
        last_link = anime.get_links()[anime.get_last_season()][anime.get_last_ep()]
        print('redirecting to:', last_link)
        self.db_engine.disconnect()

    def search_anime(self, search):
        table = self.site_anime_db.table
        field = self.site_anime_db.fields[0]

        self.db_engine.connect(self.database)
        results = self.db_engine.select(table, where=field, like=search, insensitive=True)
        self.db_engine.disconnect()

        for result in results:
            print(result[0])
        print(f'{len(results)} resultados encontrados.')

if __name__ == '__main__':
    c = Client()
    c.search_anime('boku')

