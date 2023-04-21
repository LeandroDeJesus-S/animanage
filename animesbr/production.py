import logging as log
from time import sleep
from typing import List, Dict
import re

from anime.interfaces import SerieInterface
from requester.interfaces import RequesterInterface
from parser.interfaces import ParserInterface
from anime.interfaces import ProductionsDbInterface
from database.interface import DatabaseInterface


class AnimesbrSerie(SerieInterface):
    def __init__(self, link: str, parser: ParserInterface, requester: RequesterInterface) -> None:
        super().__init__(link, parser, requester)
        self.link = link
        self.requester = requester
        self.parser = parser
        
        self._content = self.requester.get_content(link)
        
        self.last_season = 1
        self.last_ep = 1
        
    def get_last_season(self):
        default = 1
        seasons = self.parser.select_all(
            self._content, 'span.se-t.se-o', text=True, features='html.parser'
        )
        log.debug(seasons)
        if seasons is None:
            return default
        
        last_season = int(re.sub(r'[^\d]', ' ', seasons[-1]).split()[0])
        self.last_season = last_season
        return last_season

    def get_last_ep(self):
        default = 1
        eps = self.parser.select_all(
            self._content, 'div.numerando', 
            features='html.parser', text=True
        )
        if eps is None: 
            return default
        eps = list(reversed(eps))
        log.debug(eps)
        
        last_ep = int(re.sub(r'[^\d]', ' ', eps[-1]).split()[1])
        log.debug(f'last_ep: {last_ep}')
        
        self.last_ep = last_ep
        return last_ep
    
    def get_evaluation_points(self) -> float:
        default = 0.0   
        rate = self.parser.select_one(
            self._content, 'div span.dt_rating_vgs', 
            text=True, features='html.parser'
        )
        if rate is None:
            return default
        
        try:
            return float(rate)
        except ValueError:
            return default
    
    def get_category(self) -> List[str]:
        categories = self.parser.select_all(
            self._content,'div.sgeneros a', text=True, features='html.parser'
        )
        
        return categories if categories is not None else []
    
    def get_sinopse(self) -> str:
        sinopse = self.parser.select_one(
            self._content, 'div.wp-content p', text=True, features='html.parser'
        )
        log.debug(sinopse)
        if sinopse is None: return ''
        
        start = sinopse[:-1].find('.')
        log.debug(f'start: {start}')
        
        final_sinopse = sinopse[start + 1:]
        log.debug(final_sinopse)
        return final_sinopse
    
    def get_links(self) -> Dict[int, Dict[int, str]]:
        eps = self.parser.select_all(
            self._content, 'div.numerando', 
            features='html.parser', text=True
        )
        links = self.parser.select_all(
            self._content, 'div.episodiotitle a',
            features='html.parser', attr='href'
        )
        
        if eps is None or links is None: return {}
        
        f_links = {}
        for ep, link in zip(eps, links):
            se, ep = ep.split(' - ')
            se = int(re.sub(r'[^\d]', ' ', se).split()[0])  # remove invalid cases ex: 1-a return 1
            ep = int(re.sub(r'[^\d]', ' ', ep).split()[0])

            if se not in list(f_links.keys()):
                f_links.update({se: {ep: link}})
                continue
            
            f_links[se][ep] = link
            
        return f_links


class SerieDb(ProductionsDbInterface):
    def __init__(self, db_engine: DatabaseInterface) -> None:
        super().__init__(db_engine)
        self.db_engine = db_engine
        
        self.table = 'animesbr_anime'
        self.fields = ('anime', 'link')
        
    def save_production(self, data: list[dict[str, str | int | float]]) -> bool:
        try:
            self.db_engine.connect('db.sqlite')
            for d in data:
                self.db_engine.insert(
                    table=self.table, 
                    fields=self.fields, 
                    values=(*d.values(),)
                )
                sleep(.3)
            return True
        
        except Exception as error:
            print('[save_production]:', error)
            return False
        finally:
            self.db_engine.disconnect()
    
    def verify_if_exists(self, data, insensitive: bool = False, limit: int = 60) -> bool:
        result = self.db_engine.select(
            self.table, where=self.fields[0], like=data, 
            insensitive=insensitive, limit=limit
        )
        if not result:
            return False
        return True

    def get_link(self, name: str, insensitive: bool = False, limit: int = 60) -> str:
        result = self.db_engine.select(
            self.table, where=self.fields[0], like=name,
            limit=limit, insensitive=insensitive
        )
        if not result:
            return ''
        return result[0][1]
    
    def alter_name(self, name: str, new_name: str):
        self.db_engine.update(
            self.table, self.fields[0], new_name, self.fields[0], name
        )
