from parser.products import Bs4Parser, ParselParser


class Parsers:
    @staticmethod
    def use_bs4():
        bs4 = Bs4Parser()
        return bs4
    
    @staticmethod
    def use_parsel():
        parsel = ParselParser()
        return parsel
