from typing import List, Dict
import re

import requests, bs4


from interfaces import MovieInterface, SerieInterface
from requester.interfaces import RequesterInterface


class AnimesonlineMovie(MovieInterface):
    def __init__(self, link: str, parsers, requesters) -> None:
        super().__init__(link, parsers, requesters)
        self.link = link
        self.parsers = parsers
        self.requesters = requesters
        
    def get_evaluation_points(self) -> float:
        raise NotImplementedError('Not implemented yet')
    
    def get_category(self) -> List[str]:
        raise NotImplementedError('Not implemented yet')
    
    def get_sinopse(self) -> str:
        raise NotImplementedError('Not implemented yet')


class AnimesonlineSerie(SerieInterface):
    def __init__(self, link: str, parsers, requester: RequesterInterface) -> None:
        super().__init__(link, parsers, requester)
        self.link = link
        self.requester = requester.get_content(link)
        self.parsers: bs4.BeautifulSoup = parsers
        self.parse = self.parsers(self.res, 'html.parser')
        
        self.last_season = 0
        self.last_ep = 0
        
    
    @property
    def last_season(self):
        return self._last_season
    
    @last_season.setter
    def last_season(self, _):
        links = self.get_links()
        last = list(links.keys())[-1]
        self._last_season = last
    
    @property
    def last_ep(self):
        return self._last_ep
    
    @last_ep.setter
    def last_ep(self, _):
        links = self.get_links()
        last_se = list(links.keys())[-1]
        last_ep = list(links[last_se].keys())[-1]
        self._last_ep = last_ep
    
    def get_evaluation_points(self) -> float:
        rate = self.parse.select_one('div span.dt_rating_vgs').text
        try:
            return float(rate)
        except ValueError:
            rate = float(re.sub(r'[^\d .]', '', rate))
            return rate
    
    def get_category(self) -> List[str]:
        categories = self.parse.select(selector='div.sgeneros a')
        categories = [i.text for i in categories]
        return categories
    
    def get_sinopse(self) -> str:
        sinopse = self.parse.select_one(selector='div.resumotemp p')
        start: str = sinopse.text
        start = start.find('.') + 1
        return sinopse.text[start:]
    
    def get_links(self) -> Dict[int, Dict[int, str]]:
        tags = self.parse.select('div.episodiotitle a')
        links = {}
        se = 0
        for tag in tags:
            ep = int(re.sub(r'[^\d]', '', tag.text))
            link = tag.get('href')
            
            if ep == 1: se += 1
            if se not in list(links.keys()):
                links.update({se: {ep: link}})
                continue
            
            links[se].update({ep: link})
            
        return links
