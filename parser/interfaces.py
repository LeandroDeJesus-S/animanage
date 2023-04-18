from abc import ABC, abstractmethod


class ParserInterface(ABC):
    @abstractmethod
    def select_one(
        self, content: bytes|str, query: str, 
        text: bool=False, attr: str|None=None,
        **kwargs
    ): 
        """Perform a CSS selection operation on the current element

        Args:
            content (bytes | str):  A string or a file-like object 
            representing markup to be parsed.
            
            query (str): string containing css selectors
            
            text (bool, optional): if True get the text content.
             Defaults to False.
             
            attr (str | None, optional): an attribute to get the value.
             Defaults to None.
        """

    @abstractmethod
    def select_all(
        self, content: bytes|str, query: str, 
        text: bool=False, attr: str|None=None,
        **kwargs
    ):
        """Perform a CSS selection operation on the current element

        Args:
            content (bytes | str):  A string or a file-like object 
            representing markup to be parsed.
            
            query (str): string containing css selectors
            
            text (bool, optional): if True get the text content.
             Defaults to False.
             
            attr (str | None, optional): an attribute to get the value.
             Defaults to None.
        """
