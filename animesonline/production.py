from typing import List, Dict
import re
import logging as log
from pathlib import Path
import json

from anime.interfaces import MovieInterface, SerieInterface, ProductionsDbInterface
from requester.interfaces import RequesterInterface
from parser.interfaces import ParserInterface
from database.interface import DatabaseInterface


class AnimesonlineMovie(MovieInterface):
    def __init__(self, link: str, parser, requester) -> None:
        super().__init__(link, parser, requester)
        self.link = link
        self.parser = parser
        self.requester = requester
        
    def get_evaluation_points(self) -> float:
        raise NotImplementedError('Not implemented yet')
    
    def get_category(self) -> List[str]:
        raise NotImplementedError('Not implemented yet')
    
    def get_sinopse(self) -> str:
        raise NotImplementedError('Not implemented yet')


class AnimesonlineSerie(SerieInterface):
    def __init__(self, link: str, parser: ParserInterface, requester: RequesterInterface) -> None:
        super().__init__(link, parser, requester)
        self.link = link
        self.requester = requester
        self.parser = parser
        
        self.content = self.requester.get_content(link)
        self.last_season = 1
        self.last_ep = 1
        
    def get_last_season(self):
        seasons = self.parser.select_all(
            self.content, 'span.se-t', text=True, features='html.parser'
        )
        if seasons is None:
            return 1
        
        last_season = int(re.sub(r'[^\d]', ' ', seasons[-1]).split()[0])
        self.last_season = last_season
        return last_season

    def get_last_ep(self):
        eps = self.parser.select_all(
            self.content, 'div.episodiotitle a', 
            features='html.parser', text=True
        )
        if eps is None: 
            return 1
        
        last_ep = int(re.sub(r'[^\d]', ' ', eps[-1]).split()[0])
        self.last_ep = last_ep
        return last_ep
    
    def get_evaluation_points(self) -> float:        
        rate = self.parser.select_one(
            self.content, 'div span.dt_rating_vgs', 
            text=True, features='html.parser'
        )
        if rate is None:
            return 0.0
        
        try:
            return float(rate)
        except ValueError:
            return 0.0
    
    def get_category(self) -> List[str]:
        categories = self.parser.select_all(
            self.content,'div.sgeneros a', text=True, features='html.parser'
        )
        
        return categories if categories is not None else []
    
    def get_sinopse(self) -> str:
        sinopse = self.parser.select_one(
            self.content, 'div.resumotemp p', text=True, features='html.parser'
        )
        if sinopse is None: return ''
        
        start = sinopse.find('.')
        
        final_sinopse = sinopse[start + 1:]
        return final_sinopse
    
    def get_links(self) -> Dict[int, Dict[int, str]]:
        eps = self.parser.select_all(
            self.content, 'div.episodiotitle a', 
            features='html.parser', text=True
        )
        links = self.parser.select_all(
            self.content, 'div.episodiotitle a',
            features='html.parser', attr='href'
        )
        
        if eps is None or links is None: return {}
        
        f_links = {}
        se = 0
        for ep, link in zip(eps, links):
            ep = int(re.sub(r'[^\d]', '', ep))

            if ep == 1: se += 1

            if se not in list(f_links.keys()):
                f_links.update({se: {ep: link}})
                continue
            
            f_links[se][ep] = link
            
        return f_links


class SerieDb(ProductionsDbInterface):
    def __init__(self, db_engine: DatabaseInterface) -> None:
        super().__init__(db_engine)
        self.db_engine = db_engine
        
        self.table = 'animesonline_anime'
        self.fields = ('anime', 'link')
        
        self.ALIAS_FILE = Path('animesonline/aliases.json').absolute()
        
    def save_production(self, data: list[dict[str, str | int | float]]) -> bool:
        """save the productions data in database

        Args:
            data to save in database

        Obs:
            The data values should have the same order as the database fields.
        """
        try:
            for d in data:
                self.db_engine.insert(
                    table=self.table, 
                    fields=self.fields, 
                    values=(*d.values(),)
                )
            return True
        
        except Exception as error:
            log.error(error)
            return False
    
    def verify_if_exists(self, data, insensitive: bool = False, limit: int = 60) -> bool:
        """verify if a data is in the database, if it's return True if not return False

        Args:
            data (str): data to verify
            insensitive (bool, optional): if True make query with insensitive case compares. Defaults to False.
            limit (int, optional): limit of data to verify. Defaults to 60.

        Returns:
            bool: True if exists, False if not
        """
        result = self.db_engine.select(
            self.table, where=self.fields[0], like=data, 
            insensitive=insensitive, limit=limit
        )
        if not result:
            return False
        return True

    def get_link(self, name: str, insensitive: bool = False, limit: int = 60) -> str:
        """get data from database

        Args:
            name: production name to get the link
            insensitive (bool, optional): if True make query with insensitive case compares. Defaults to False.
            limit (int, optional): limit of data to verify. Defaults to 60.

        Returns:
            str: link founded by name
        """
        anime = self.get_alias(name)
        result = self.db_engine.select(
            self.table, where=self.fields[0], like=anime,
            limit=limit, insensitive=insensitive
        )
        log.debug(f'result: {result}')
        if not result:
            return ''
        result_name = result[0][0]
        if result_name.lower() != anime.lower():
            print(f'Você quis dizer \033[33m"{result_name}"\033[m?')
            log.info(f'found {result_name} not {anime}')
            return ''
        
        return result[0][1]
    
    def set_alias(self, alias: str, to: str) -> bool:
        """set an alias to an anime from database

        Args:
            alias (str): the alias to the anime
            to (str): anime which receives the alias

        Returns:
            bool: True if there weren't errors
        """
        try:
            data = self._get_aliases()
            data.update({alias: to})
            
            self._write_alias(data)
            return True
        
        except FileNotFoundError:
            self._write_alias({})
            return False
        
        except Exception as error:
            log.error(error)
            return False

    def get_alias(self, alias: str) -> str:
        """get an anime by alias

        Args:
            alias (str): alias of the anime

        Returns:
            str: the anime name in database owned of the alias
            if not found return the alias argument with no changes
        """
        if not self.ALIAS_FILE.exists():
            self._write_alias({})
            
        with open(self.ALIAS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        key = [k for k in data if k.lower() == alias.lower()]
        return data.get(key[0]) if key else alias
    
    def _get_aliases(self) -> dict[str, str]:
        """get all data of the alias file"""
        with open(self.ALIAS_FILE, encoding='utf-8') as f:
            data = json.load(f)
        return data
        
    def _write_alias(self, data: dict[str, str]) -> None:
        """register the alias data after update"""
        with open(self.ALIAS_FILE, 'w+', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
