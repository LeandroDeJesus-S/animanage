from typing import List, Dict
import re

from anime.interfaces import MovieInterface, SerieInterface
from requester.interfaces import RequesterInterface
from parser.interfaces import ParserInterface


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
        if seasons is None:
            return default
        
        last_season = int(re.sub(r'[^\d]', ' ', seasons[-1]).split()[0])
        self.last_season = last_season
        return last_season
    

    def get_last_ep(self):
        default = 1
        eps = self.parser.select_all(
            self._content, 'div.episodiotitle a', 
            features='html.parser', text=True
        )
        if eps is None: 
            return default
        
        last_ep = int(re.sub(r'[^\d]', ' ', eps[-1]).split()[0])
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
            self._content, '.wp-content p', text=True, features='html.parser'
        )
        if sinopse is None: return ''
        
        start = sinopse.find('.')
        
        final_sinopse = sinopse[start + 1:]
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
