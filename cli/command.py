from abc import ABC, abstractmethod
from itertools import zip_longest
from pathlib import Path
import time
from typing import Any
import webbrowser

from available_sites.sites import Sites
from database.databases import SQLite
from history.history import WatchHistory
from website.interface import SiteInterface


class Anime:
    """Class for managing anime operations like 
    redirects, information, etcetera.
    """
    def __init__(self) -> None:
        self.current_site = Sites.site_active()
        self.site: SiteInterface = Sites[self.current_site].value
        self.series_db = self.site.get_series_db()
        
        self.database = str(Path('db.sqlite').absolute())
        self.db = SQLite()
        
    def watch(self, name: str, se=1, ep=1) -> None:
        """redirect to the episode of the anime.

        Args:
            name (str): anime name
            se (int, optional): season number. Defaults to 1.
            ep (int, optional): episode number. Defaults to 1.
        """
        self.db.connect(self.database)
        link = self.series_db.get_link(name, insensitive=True)
        self.db.disconnect()
        
        if not link:
            print('\033[31mNenhum resultado encontrado.\033[m')
            return
        
        anime = self.site.get_anime(link)
        
        try:
            final_link = anime.get_links()[se][ep]
            webbrowser.open(final_link)
            
        except KeyError:
            print('\033[31mTemporada ou episódio não encontrado.\033[m')
            
    def watch_latest(self, name: str) -> None:
        """redirect to the most recent episode of the anime.

        Args:
            name (str): anime name
        """
        self.db.connect(self.database)
        anime_link = self.series_db.get_link(name, insensitive=True)
        self.db.disconnect()
        
        if not anime_link:
            print('\033[31mNenhum resultado encontrado.\033[m')
            return
        
        anime_ = self.site.get_anime(anime_link)
        
        last_se, last_ep = anime_.get_last_season(), anime_.get_last_ep()
        last_link = anime_.get_links()[last_se][last_ep]
        webbrowser.open(last_link)
        WatchHistory.register(name, last_se, last_ep)
    
    def search(self, search: str):
        """search by an anime in database

        Args:
            search (str): anime name
        """
        table = self.series_db.table
        field = self.series_db.fields[0]

        self.db.connect(self.database)
        results = self.db.select(
            table, where=field, like=search, insensitive=True
        )
        self.db.disconnect()
        
        n_results = len(results)

        for result in results:
            print(result[0])            
        
        color = '\033[31m' if n_results == 0 else '\n\033[32m'
        print(f'{color}{n_results}\033[m resultados encontrados.')
    
    def get_info(self, anime: str):
        """get evaluation points, gender, most recent ep and 
        the summary of the anime.

        Args:
            anime (str): anime name
        """
        self.db.connect(self.database)
        link = self.series_db.get_link(anime, insensitive=True)
        self.db.disconnect()
        
        if not link:
            print('\033[31mNenhum resultado encontrado.\033[m')
            return
        
        animeobj = self.site.get_anime(link)
        self.__print_info(animeobj)
    
    def __print_info(self, animeobj):
        """make a print in a table format"""
        h1, h2, h3, h4 = 'Avaliação', 'Gênero', 'Ep atual', 'Sinopse'
        evaluation = animeobj.get_evaluation_points()
        gender = animeobj.get_category()
        
        last_ep = animeobj.get_last_ep()
        last_se = animeobj.get_last_season()
        actual_ep = f'SE{last_se}/EP{last_ep}'
        
        sinopse = animeobj.get_sinopse()
        line = ''
        lines = []
        for word in sinopse.split():
            line += f'{word} '

            if len(line) > 15:
                lines.append(line)
                line = ''
            else:
                word_index = sinopse.find(word)
                to_end = len(sinopse[word_index:])
                if to_end < 20:
                    lines.append(line)
        
        print_line = lambda: print('+' + '-' * 73 + '+')
        
        print_line()
        print(f'|{h1:^11}|{h2:^17}|{h3:^11}|{h4:^31}|')
        print_line()
        for e, g, a, s in zip_longest([evaluation], gender, 
                                      [actual_ep], lines, fillvalue=''):
            print(f'|{e:^11}|{g:^17}|{a:^11}|{s:^31}|')
        print_line()
    
    def list_episodes(self, anime: str):
        """list the number of episode to each season

        Args:
            anime (str): anime name
        """
        self.db.connect(self.database)
        link = self.series_db.get_link(anime, insensitive=True)
        
        if not link:
            print('\33[31mNenhum resultado encontrado.\033[m')
            return
        
        animeobj = self.site.get_anime(link)
        self.db.disconnect()
        
        data = animeobj.get_links().items()
        
        line = lambda: print('+' + '~' * 17 + '+')
        h1, h2 = 'SE', 'EPs'
        line()
        print(f'|{h1:^8}|{h2:^8}|')
        line()
        for se, eps in data:
            print(f'|{se:^8}|{len(eps):^8}|')
        line()

    def change_name(self, name: str, to: str):
        """change the name of the anime in database.

        Args:
            name (str): anime name in database
            to (str): new name to the anime
        """
        self.db.connect(self.database)
        anime = self.db.select(self.series_db.table,
                              where=self.series_db.fields[0],
                              like=name)
        
        if not anime:
            print('\033[31mNenhum resultado encontrado.\033[m')
            return
        
        old = f'\033[33m"{anime[0][0]}"\033[m'
        new = f'\033[33m"{to}"\033[m'
        confirm = input(f'Deseja alterar {old} para {new}?[s/n]: ')
        
        if confirm.lower() == 's':
            self.series_db.alter_name(name, to.title())
            print('\033[32mAlterado com sucesso!\033[m')
        
        self.db.disconnect()

    def add_anime(self, name: str, url: str):
        """add a new anime in database.

        Args:
            name (str): anime name
            url (str): anime homepage
        """
        print(f'anime: {name}\nurl: {url}')
        c = input(f'Confirmar?> (s/n): ')
        
        if c.lower() == 'n' or c.lower() != 's':
            print('Tente novamente!')
            return
        
        name = name.strip().title()
        url = url.strip()
        
        self.db.connect(self.database)
        self.series_db.save_production([{'anime': name, 'url': url}])
        self.db.disconnect()
        print(f'\033[32m"{name}"\033[m adicionado com sucesso.')


class ICommand(ABC):
    @abstractmethod
    def execute(self): pass
    
    
class WatchAnime(ICommand):
    def __init__(self,  anime: Anime, name: str, se=1, ep=1) -> None:
        self.anime = anime
        self.name = name
        self.season = se
        self.episode = ep
        
    def execute(self) -> None:
        self.anime.watch(self.name, self.season, self.episode)
        WatchHistory.register(self.name, self.season, self.episode)
    
    
class WatchLatestEp(ICommand):
    def __init__(self,  anime: Anime, name: str) -> None:
        self.anime = anime
        self.name = name
        
    def execute(self) -> None:
        self.anime.watch_latest(self.name)        


class SearchAnime(ICommand):
    def __init__(self,  anime: Anime, name: str) -> None:
        self.anime = anime
        self.name = name
        
    def execute(self) -> None:
        self.anime.search(self.name)


class GetInfo(ICommand):
    def __init__(self,  anime: Anime, name: str) -> None:
        self.anime = anime
        self.name = name
        
    def execute(self) -> None:
        self.anime.get_info(self.name)


class ListEpisodes(ICommand):
    def __init__(self,  anime: Anime, name: str) -> None:
        self.anime = anime
        self.name = name
        
    def execute(self) -> None:
        self.anime.list_episodes(self.name)


class ChangeName(ICommand):
    def __init__(self, anime: Anime, name: str, to: str) -> None:
        self.anime = anime
        self.name = name
        self.to = to
    
    def execute(self) -> None:
        self.anime.change_name(self.name, self.to)


class AddAnime(ICommand):
    def __init__(self, anime: Anime, name: str, url: str) -> None:
        self.anime = anime
        self.name = name
        self.url = url
    
    def execute(self) -> None:
        self.anime.add_anime(self.name, self.url)
    

class Releases:
    def __init__(self) -> None:
        self.current_site = Sites.site_active()
        self.site: SiteInterface = Sites[self.current_site].value
        
        self.db_engine = SQLite()
        self.database = str(Path('db.sqlite').absolute())
        
        self.site_ep_release_db = self.site.get_ep_releases_db()
        self.site_anime_release_db = self.site.get_anime_releases_db()

    def list_ep_releases(self):
        """show episodes from page of episode releases.
        """
        releases = self.site.get_ep_releases()
        
        self.db_engine.connect(self.database)
        
        for release in reversed(releases):
            title = str(*release.values())
            if self.site_ep_release_db.verify_if_exists(title):
                print(title)
                continue

            print(f'\033[32m{title}\033[m')
            
        self.db_engine.disconnect()

    def list_anime_releases(self):
        """show animes from anime releases page.
        """
        releases = self.site.get_anime_releases()
        
        self.db_engine.connect(self.database)
        for anime in reversed(releases):
            name, rate = anime.values()
            if not self.site_anime_release_db.verify_if_exists(name):
                name = f'\033[36m{name}\033[m'

            if isinstance(rate, int|float) and rate > 0:
                rate = f' ~ {self.__colorize_rate(rate)}'
            else:
                rate = ''
            
            print(f'{name}{rate}')

        self.db_engine.disconnect()
    
    @staticmethod
    def __colorize_rate(rate: float) -> str:
        """set a color on the rate.

        Args:
            rate (float): rate value.

        Returns:
            str: rate colored by ascii code.
        """
        if rate < 5:
            color_code = "\033[31m"  # red
        elif rate < 7:
            color_code = "\033[33m"  # yellow
        elif rate < 9:
            color_code = "\033[32m"  # green
        else:
            color_code = "\033[35m"  # magenta
            
        return f"{color_code}{rate}\033[m"

    def update(self):
        """get the animes and episodes on the site and save case
        the anime is not in database.
        """
        start_time = time.time()
        self.db_engine.connect(self.database)
        
        print('Buscando animes...')
        anime_releases = self.site.get_anime_releases()
        print('Buscando episódios...')
        ep_releases = self.site.get_ep_releases()
        print('Salvando na base de dados...')
        tot_updates = 0
        for anime, ep in zip_longest(anime_releases, ep_releases):
            name = anime['anime']
            anime_exists = self.site_anime_release_db.verify_if_exists(name)
            if not anime_exists: 
                self.site_anime_release_db.save_releases([anime])
                tot_updates += 1
            
            title = ep['title']
            ep_exists = self.site_ep_release_db.verify_if_exists(title)
            if not ep_exists:
                self.site_ep_release_db.save_releases([ep])
                tot_updates += 1
        
        self.db_engine.disconnect()
        
        tot_time = time.time() - start_time
        print('\033[32mTudo pronto! :)\033[m')
        print(f'\033[37m{tot_updates} updates in {tot_time:.2f} seconds\033[m')
        

class ListEpisodeReleases(ICommand):
    def __init__(self, releases: Releases) -> None:
        self.releases = releases
        
    def execute(self):
        self.releases.list_ep_releases()


class ListAnimeReleases(ICommand):
    def __init__(self, releases: Releases) -> None:
        self.releases = releases
        
    def execute(self):
        self.releases.list_anime_releases()


class UpdateReleases(ICommand):
    def __init__(self, releases: Releases) -> None:
        self.releases = releases
        
    def execute(self) -> None:
        self.releases.update()


class WebSites:
    """do website operations"""
    def __init__(self):
        self.sites = Sites
        self.site_active = self.sites.site_active()
    
    def list_sites(self):
        """show websites available
        """
        for site in self.sites:
            site_name =  site.name
            if site_name == self.site_active:
                
                site_name = f'\033[32m*\033[m {site_name}'
                
            else:
                site_name = '  ' + site_name
                
            print(site_name)
            
    def change_site(self, site: str):
        """change the website in use.

        Args:
            site (str): site name
        """
        self.sites.set_site(site)


class ListSites(ICommand):
    def __init__(self, sites: WebSites):
        self.sites = sites
        
    def execute(self) -> None:
        self.sites.list_sites()
        

class ChangeSite(ICommand):
    def __init__(self, name, sites: WebSites):
        self.name = name
        self.sites = sites
        
    def execute(self):
        self.sites.change_site(self.name)


class History:
    """manage the history"""
    def __init__(self, filter: str|None=None) -> None:
        self.filter = filter
        self.history = WatchHistory()
        
    def show_history(self) -> None:
        """show the history of last redirects"""
        self.history.show(self.filter)
    
    def add_to_history(self, name, se, ep) -> None:
        """add an anime to history"""
        self.history.register(name, se, ep)
    
    def remove_from_history(self, name) -> None:
        """remove an anime from history"""
        self.history.remove(name)


class ShowHistory(ICommand):
    def __init__(self, history: History):
        self.history = history
        
    def execute(self):
        self.history.show_history()
    

class AddToHistory(ICommand):
    def __init__(self, history: History, name: str, se: int, ep: int) -> None:
        self.history = history
        self.name = name
        self.se = se
        self.ep = ep

    def execute(self) -> None:
        self.history.add_to_history(self.name, self.se, self.ep)
    

class RemoveFromHistory(ICommand):
    def __init__(self, history: History, name: str) -> None:
        self.history = history
        self.name = name

    def execute(self) -> None:
        self.history.remove_from_history(self.name)


class Invoker:
    def __init__(self) -> None:
        self._commands: dict[Any, ICommand] = {}
    
    def add_command(self, key, command: ICommand):
        self._commands.update({key: command})
        
    def execute_command(self, key):
        self._commands[key].execute()
