try:
    import sys, os
    sys.path.append(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'
            )
        )
    )
except: pass

from time import sleep
from typing import List, Dict
import re

from anime.interfaces import SerieInterface
from requester.interfaces import RequesterInterface
from parser.interfaces import ParserInterface
from anime.interfaces import ProductionsDbInterface
from database.interface import DatabaseInterface


class AnimesonlineOnlineSerie(SerieInterface):
    def __init__(self, link: str, parser: ParserInterface, requester: RequesterInterface) -> None:
        super().__init__(link, parser, requester)
        self.link = link
        self.requester = requester
        self.parser = parser
                
        self.last_season = 1
        self.last_ep = 1

        self.content = self.requester.get_content(self.link, type='text')

    def get_last_season(self):
        data = self.get_links()
        last_se = list(data.keys())[-1]
        self.last_season = last_se
        return last_se

    def get_last_ep(self):
        data = self.get_links()
        last_se = list(data.keys())[-1]
        last_ep = list(data[last_se].keys())[-1]
        self.last_ep = last_ep
        return last_ep

    def get_evaluation_points(self) -> float:
        return 0.0

    def get_category(self) -> List[str]:
        categories = self.parser.select_all(
            self.content, 'div.sgeneros a', text=True
        )

        return categories if categories is not None else []

    def get_sinopse(self) -> str:
        sinopse = self.parser.select_one(
            self.content, 'div.wp-content p', text=True
        )
        if sinopse is None:
            return ''

        sinopse = re.sub(r'\bAssistir(.*?)Anime Completo\b', '', sinopse)
        return sinopse

    def get_links(self) -> Dict[int, Dict[int, str]]:
        eps = self.parser.select_all(
            self.content, 'div.episodiotitle a', text=True
        )

        links = self.parser.select_all(
            self.content, 'div.episodiotitle a', attr='href'
        )

        if eps is None or links is None:
            return {}

        f_links = {}
        se = 0
        for ep, link in zip(eps, links):
            ep = int(re.sub(r'\D', '', ep))

            if ep == 1:
                se += 1

            if se not in list(f_links.keys()):
                f_links.update({se: {ep: link}})
                continue

            f_links[se][ep] = link

        return f_links


class SerieDb(ProductionsDbInterface):
    def __init__(self, db_engine: DatabaseInterface) -> None:
        super().__init__(db_engine)
        self.db_engine = db_engine

        self.table = 'animesonline_online_anime'
        self.fields = ('anime', 'link')

    def save_production(self, data: list[dict[str, str | int | float]]):
        for d in data:
            self.db_engine.insert(
                table=self.table,
                fields=self.fields,
                values=(*d.values(),)
            )
            sleep(.1)

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
