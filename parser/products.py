from typing import Union
from bs4 import BeautifulSoup, ResultSet, Tag
from parsel import Selector

from .interfaces import ParserInterface


class Bs4Parser(ParserInterface):
    def select_one(
        self, content: bytes | str, 
        query: str, text: bool = False, 
        attr: str | None = None, **kwargs) -> Tag | str | list[str] | None:
        
        if attr is not None and text:
            raise ValueError('<text> and <attr> cannot both be sent')
        
        if not kwargs.get('features'):
            kwargs.update({'features': 'html.parser'})
                          
        soup = BeautifulSoup(content, **kwargs)
        result = soup.select_one(query)
        
        if attr is not None and result is not None: 
            return result.get(attr, None)
        
        if text and result is not None:
            return result.text
        
        return result


    def select_all(
        self, content: bytes | str, 
        query: str, text: bool = False, 
        attr: str | None = None, **kwargs) -> ResultSet[Tag] | list[str | list[str] | None]:
        
        if attr is not None and text:
            raise ValueError('<text> and <attr> cannot both be sent')
        
        if not kwargs.get('features'):
            kwargs.update({'features': 'html.parser'})
    
        soup = BeautifulSoup(content, **kwargs)
        result = soup.select(query)
        if attr is not None and isinstance(result, ResultSet): 
            return [tag.get(attr) for tag in result]
        
        elif text:
            return [tag.text for tag in result]
                
        return result


class ParselParser(ParserInterface):
    def select_one(
        self, content: str, 
        query: str, text: bool = False, 
        attr: str | None = None, **kwargs) -> str | None:
        if attr is not None and text:
            raise ValueError('<text> and <attr> cannot both be sent')
        
        parsel = Selector(content, **kwargs)
        if text and '::text' not in query:
            query += '::text'
            
        result = parsel.css(query).get()
        
        if attr is not None: 
            result = parsel.css(query).attrib.get(attr)
        
        return result


    def select_all(
        self, content: str, 
        query: str, text: bool = False, 
        attr: str | None = None, **kwargs) -> list[str] | None:
        
        if (attr is not None) and (text or '::text' in query):
            raise ValueError('<text> and <attr> cannot both be sent')
        
        if attr is not None and '::attr' not in query: 
            query += f'::attr({attr})'
            
        parsel = Selector(content, **kwargs)
        if text and '::text' not in query:
            query += '::text'

        result = parsel.css(query)
            
        return result.getall()
