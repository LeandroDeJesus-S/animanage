from typing import Literal

from .interfaces import RequesterInterface

import requests, httpx


class Requests(RequesterInterface):
    def get_content(self, url: str, type: Literal['bytes', 'text']='bytes', **kwargs) -> bytes|str:
        types = ['bytes', 'text']
        if type.lower() not in types:
            raise TypeError(f'Invalid type. Available types are {types}')
        
        response = requests.get(url, **kwargs)
        return_types = {'bytes': response.content, 'text': response.text}
        return return_types[type]


class HttpX(RequesterInterface):        
    def get_content(self, url: str, type: Literal['bytes', 'text']='bytes', **kwargs) -> bytes|str:
        types = ['bytes', 'text']
        if type.lower() not in types:
            raise TypeError(f'Invalid type. Available types are {types}')
        
        response = httpx.get(url, **kwargs)
        return_types = {'bytes': response.content, 'text': response.text}
        return return_types[type]
