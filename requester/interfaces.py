from abc import ABC, abstractmethod
from typing import Literal

class RequesterInterface(ABC):
        
    @abstractmethod
    def get_content(self,url: str, type: Literal['bytes', 'text']='bytes', **kwargs) -> bytes | str:
        """Do a get request and return the content in the given type

        Args:
            url (str): the url to get the content
            type (Literal['bytes', 'text']): if is bytes return the content
            in bytes format, if is str return the content in text format
            
            default is bytes

        rType: bytes or str: 
        """
