try:
    import sys, os
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..'
            )
        )
    )
except: pass

from time import sleep
import os
from typing import Literal
from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By 

from parser.interfaces import ParserInterface


class SeleniumParser(ParserInterface):
    def __init__(self):
        self.options = Options()
        args = ['--incognito', '--headless', '--disable-gpu', '--no-sandbox', 
                '--lang=pt-BR', '--disable-dev-shm-usage']
        
        for arg in args:
            self.options.add_argument(arg)
            
        self.service = Service('selenium/msedgedriver.exe')
        self.browser = Edge(service=self.service, options=self.options)
        
    def select_all(
        self, content: str, 
        query: str, text: bool = False, 
        attr: str | None = None, **kwargs
    ):
        by = kwargs.get('by')
        by = by if by is not None else 'xpath'

        self.browser.get(content)

        sleep(.5)

        elements = self.browser.find_elements(value=query, by=by)
        sleep(.1)
        result = [element.text for element in elements] if text else elements
        if attr:
            result = [element.get_attribute(attr) for element in elements]
            
        self.browser.close()
        self.browser.quit()
        os.system('cls')
        return result
    
    def select_one(
        self, content: str, 
        query: str, text: bool = False, 
        attr: str | None = None, **kwargs
    ):
        by = kwargs.get('by')
        by = by if by is not None else 'xpath'

        self.browser.get(content)
        
        sleep(.5)

        element = self.browser.find_element(value=query, by=by)
        sleep(.1)
        
        result = element.text if text else element
        if attr:
            result = element.get_attribute(attr)
            
        self.browser.close()
        self.browser.quit()
        os.system('cls')
        return result
