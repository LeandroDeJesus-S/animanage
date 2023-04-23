from itertools import zip_longest
import logging as log
from pathlib import Path
import time
import webbrowser

from anime.interfaces import ProductionsDbInterface
from available_sites import sites
from database.databases import SQLite
from parser.factory import Parsers
from requester.factory import Requesters
from website.interface import SiteInterface

parser = Parsers.use_bs4()
requester = Requesters.use_requests()


class CliFunctions:
    def __init__(self):
        self.sites = sites.Sites
        self.site_active = self.sites.site_active()
        log.info(f'total sites : {len(self.sites)} | active : {self.site_active}')

        self.db_engine = SQLite()
        self.database = str(Path('db.sqlite').absolute())
        log.debug(f'db using : {self.db_engine.__class__} | path : {self.database}')

        self.site: SiteInterface = self.sites[self.site_active].value
        self.site_anime_db: ProductionsDbInterface = self.site.get_series_db()
        self.site_ep_release_db = self.site.get_ep_releases_db()
        self.site_anime_release_db = self.site.get_anime_releases_db()
        log.debug(f'site class : {self.site.__class__}')
        log.debug(f'site  : {self.site.__class__}')
        log.debug(f'site anime db : {self.site_anime_db.__class__}')
        log.debug(f'site episode release db : {self.site_ep_release_db.__class__}')
        log.debug(f'site anime release db : {self.site_anime_release_db.__class__}')
                
    def watch(self, anime, se=1, ep=1):
        log.debug(f'anime : {anime} | se : {se} | ep : {ep}')
        
        self.db_engine.connect(self.database)
        link = self.site_anime_db.get_link(anime, insensitive=True)
        self.db_engine.disconnect()
        log.debug(f'anime link found : {link}')
        
        if not link:
            print('\033[31mNenhum resultado encontrado.\033[m')
            return

        anime = self.site.get_anime(link)
        log.debug(f'anime class : {anime.__class__}')
        
        links = anime.get_links()
        
        try:
            link = links[se][ep]
            webbrowser.open(link)
            log.info(f'redirected to : {link}')
            
        except KeyError:
            print('\033[31mTemporada ou episódio não encontrado.\033[m')
            log.info(f'link not found')

    def list_ep_release(self):
        releases = self.site.get_ep_releases()
        log.debug(f'found releases: {len(releases)}')
        
        self.db_engine.connect(self.database)
        
        for release in releases:
            title = str(*release.values())
            if self.site_ep_release_db.verify_if_exists(title):
                print(title)
                continue

            print(f'\033[32m{title}\033[m')
        log.debug('releases of ep listed successfully')
        self.db_engine.disconnect()

    def list_anime_release(self):
        releases = self.site.get_anime_releases()
        log.debug(f'found releases: {len(releases)}')
        
        self.db_engine.connect(self.database)
        for anime in releases:
            name, rate = anime.values()
            if not self.site_anime_release_db.verify_if_exists(name):
                name = f'\033[36m{name}\033[m'

            if isinstance(rate, int|float) and rate > 0:
                rate = f' ~ {self.__colorize_rate(rate)}'
            else:
                rate = ''
            
            print(f'{name}{rate}')
        
        log.debug('releases of animes listed successfully')
        self.db_engine.disconnect()

    @staticmethod
    def __colorize_rate(rate: float) -> str:
        if rate < 5:
            color_code = "\033[31m"  # red
        elif rate < 7:
            color_code = "\033[33m"  # yellow
        elif rate < 9:
            color_code = "\033[32m"  # green
        else:
            color_code = "\033[35m"  # magenta
            
        return f"{color_code}{rate}\033[m"

    def watch_latest(self, anime):
        log.debug(f'anime : {anime}')
        
        self.db_engine.connect(self.database)
        anime_link = self.site_anime_db.get_link(anime, insensitive=True)
        self.db_engine.disconnect()
        log.debug(f'anime link found : {anime_link}')
        
        if not anime_link:
            print('\033[31mNenhum resultado encontrado.\033[m')
            return
        
        anime = self.site.get_anime(anime_link)
        log.debug(f'anime class : {anime.__class__}')
        
        last_se, last_ep = anime.get_last_season(), anime.get_last_ep()
        log.debug(f'last se found : {last_se} last ep found : {last_ep}')
        last_link = anime.get_links()[last_se][last_ep]
        webbrowser.open(last_link)
        log.info(f'redirected to : {last_link}')

    def search(self, search):
        log.debug(f'search : "{search}"')
        
        table = self.site_anime_db.table
        field = self.site_anime_db.fields[0]
        log.debug(f'table : {table} | field : {field}')

        self.db_engine.connect(self.database)
        results = self.db_engine.select(
            table, where=field, like=search, insensitive=True
        )
        self.db_engine.disconnect()
        
        n_results = len(results)
        log.info(f'{n_results} results found')

        for result in results:
            print(result[0])            
        
        color = '\033[31m' if n_results == 0 else '\n\033[32m'
        print(f'{color}{n_results}\033[m resultados encontrados.')
    
    def get_info(self, anime):
        log.debug(f'anime : {anime}')
        
        self.db_engine.connect(self.database)
        link = self.site_anime_db.get_link(anime, insensitive=True)
        self.db_engine.disconnect()
        log.debug(f'link found : {link}')
        
        if not link:
            print('\033[31mNenhum resultado encontrado.\033[m')
            return
        
        anime = self.site.get_anime(link)
        log.debug(f'anime class : {anime.__class__}')
        self.__print_info(anime)
    
    def __print_info(self, animeobj):
        h1, h2, h3, h4 = 'Avaliação', 'Gênero', 'Ep atual', 'Sinopse'
        evaluation = animeobj.get_evaluation_points()
        gender = animeobj.get_category()
        
        last_ep = animeobj.get_last_ep()
        last_se = animeobj.get_last_season()
        actual_ep = f'SE{last_se}/EP{last_ep}'
        
        sinopse = animeobj.get_sinopse()
        log.debug(
            f'evaluation points : {evaluation} | gender : {gender}'
            f'actual ep : {actual_ep} | sinopse : "{sinopse[:15]}...{sinopse[-15:]}"'
        )
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
        log.debug('called successfully')
    
    def list_episodes(self, anime):
        self.db_engine.connect(self.database)
        
        link = self.site_anime_db.get_link(anime, insensitive=True)
        log.debug(f'anime link : {link}')
        
        if not link:
            print('\33[31mNenhum resultado encontrado.\033[m')
            return
        
        anime = self.site.get_anime(link)
        log.debug(f'anime class : {anime.__class__}')
        
        data = anime.get_links().items()
        log.debug(f'data mapping : {data.mapping}')
        
        line = lambda: print('+' + '~' * 17 + '+')
        h1, h2 = 'SE', 'EPs'
        line()
        print(f'|{h1:^8}|{h2:^8}|')
        line()
        for se, eps in data:
            print(f'|{se:^8}|{len(eps):^8}|')
        line()
        
        log.debug(f'eps listed successfully')    
        self.db_engine.disconnect()
        
    def changename(self, name: str, to: str):
        log.debug(f'name : "{name}" | to : "{to}"')
        
        self.db_engine.connect(self.database)
        anime = self.db_engine.select(self.site_anime_db.table,
                              where=self.site_anime_db.fields[0],
                              like=name)
        log.debug(f'db result of fetch by name : {anime}')
        
        if not anime:
            print('\033[31mNenhum resultado encontrado.\033[m')
            return
        
        old = f'\033[33m"{anime[0][0]}"\033[m'
        new = f'\033[33m"{to}"\033[m'
        confirm = input(f'Deseja alterar {old} para {new}?[s/n]: ')
        log.debug(f'user confirmation : {confirm}')
        
        if confirm.lower() == 's':
            self.site_anime_db.alter_name(name, to)
            print('\033[32mAlterado com sucesso!\033[m')
            log.info(f'"{name}" altered to "{to}"')
        
        self.db_engine.disconnect()
        log.debug('function ended')
        
    def update(self):
        log.debug('update starting')
        start_time = time.time()
        self.db_engine.connect(self.database)
        
        print('Buscando animes...')
        anime_releases = self.site.get_anime_releases()
        print('Buscando episódios...')
        ep_releases = self.site.get_ep_releases()
        log.debug(
            f'anime releases: {len(anime_releases)}'
            f' | ep releases: {len(ep_releases)}'
        )
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
        log.info(f'{tot_updates} updates in {tot_time:.2f} seconds')
    
    def list_sites(self):
        log.debug('listing sites')
        for site in self.sites:
            site_name =  site.name
            if site_name == self.site_active:
                log.debug(f'active site : {site_name}')
                
                site_name = f'\033[32m*\033[m {site_name}'
                
            else:
                site_name = '  ' + site_name
                
            print(site_name)
        log.debug(f'listed sites : {len(self.sites)}')

    def change_site(self, site: str):
        self.sites.set_site(site)
        log.debug(f'site changed to : {site}')

    def add_anime(self, name: str, url: str):
        print(f'Verifique se o link esta correto: {url}')
        c = input(f'> (s/n): ')
        
        if c.lower() == 'n' or c.lower() != 's':
            print('Tente novamente!')
            return
        
        name = name.strip().title()
        url = url.strip()
        log.debug(f'name : {name} | url : {url}')
        
        self.db_engine.connect(self.database)
        self.site_anime_db.save_production([{'anime': name, 'url': url}])
        self.db_engine.disconnect()
        print(f'\033[32m"{name}"\033[m] adicionado com sucesso.')
