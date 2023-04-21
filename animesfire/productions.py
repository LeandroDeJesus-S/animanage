try:
    import sys, os
    sys.path.append(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'
            )
        )
    )
except: pass

import logging as log
from time import sleep
from typing import List, Dict
import re

from anime.interfaces import SerieInterface
from requester.interfaces import RequesterInterface
from parser.interfaces import ParserInterface
from anime.interfaces import ProductionsDbInterface
from database.interface import DatabaseInterface


class Animefire(SerieInterface):
    def __init__(self, link: str, parser: ParserInterface, requester: RequesterInterface) -> None:
        super().__init__(link, parser, requester)
        self.link = link
        self.requester = requester
        self.parser = parser
                
        self.last_season = 1
        self.last_ep = 1
        
    def get_last_season(self):
        default = 1
        seasons = self.parser.select_all(
            self.link, 'span.se-t.se-o', text=True, 
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
            self.link, 'div.numerando', 
            text=True
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
            self.link, 
            '//*[@id="anime_score"]', 
            text=True
        )
        
        if rate is None:
            return default
        
        try:
            return float(rate)
        except ValueError:
            return default
    
    def get_category(self) -> List[str]:
        categories = self.parser.select_all(
            self.link,
            'spanGeneros', 
            text=True, by='class name'
        )

        return categories if categories is not None else []
    
    def get_sinopse(self) -> str:
        sinopse = self.parser.select_one(
            self.link, 
            '/html/body/div[2]/div[1]/div/div[2]/div[3]/div/div/span',
            text=True, by='xpath'
        )
        print(sinopse)
        if sinopse is None: return ''

        print(sinopse)
        return sinopse.replace('\n', '')
    
    def get_links(self) -> Dict[int, Dict[int, str]]:
        eps = self.parser.select_all(
            self.link, 'article.post header.entry-header span.num-epi', 
            text=False
        )
        print('eps : ', eps)
        links = self.parser.select_all(
            self.link, 'before a.lnk-blk',
            attr='href'
        )
        print('links : ', links)
        
        if eps is None or links is None: return {}
        
        f_links = {}
        for ep, link in zip(eps, links):
            print(ep, link)
            se, ep = ep.split('x')
            se = int(re.sub(r'[^\d]', ' ', se).split()[0])  # remove invalid cases ex: 1-a return 1
            ep = int(re.sub(r'[^\d]', ' ', ep).split()[1])

            if se not in list(f_links.keys()):
                f_links.update({se: {ep: link}})
                continue
            
            f_links[se][ep] = link
            
        return f_links


if __name__ == '__main__':
    from parser.factory import Parsers
    from requester.factory import Requesters
    from pprint import pprint
    
    test = Animefire('https://animesflix.net/assistir/1725-niehime-to-kemono-no-ou', Parsers.use_bs4(), Requesters.use_httpx())
    pprint(test.get_links())
