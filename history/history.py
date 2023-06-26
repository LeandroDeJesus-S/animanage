import json
import os.path
from datetime import datetime
from locale import LC_ALL, setlocale
import logging as log
from pathlib import Path

# TODO: sometimes the history file is wrote with extra chars

class WatchHistory:
    MAX_CHAR_SHOW = 15
    history_file = Path('history').absolute() / 'history.json'
    
    def __init__(self) -> None:
        self.verify_file_exists()
    
    @classmethod
    def verify_file_exists(cls):
        if not Path(cls.history_file).is_file():
            cls.write([{}])
        
    
    @classmethod
    def data(cls) -> list[dict]:
        """get the content of the history file"""
        with open(cls.history_file, 'r+', encoding='utf-8') as f:
            filedata = json.load(f)
            log.debug(f'history data found : {len(filedata)}')
        return filedata
    
    @classmethod
    def write(cls, data: list[dict], file=history_file) -> bool|None:
        """write the data in the history file, creating case it doesn't exists
        
        returns:
            True if operation is done without errors else return None
        """
        with open(file, 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
        
    @classmethod
    def register(cls, anime: str, se: int, ep: int):
        """register a new anime in the history

        Args:
            anime (str): anime name
            se (int): season
            ep (int): episode

        Returns:
            bool: True if the operation is succeeds
        """
        loc = setlocale(LC_ALL, '')
        log.debug(f'locale : {loc}')
        date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
        data = cls.data()
        for d in data:
            if d['anime'].lower() != anime.lower():
                continue
            
            d['se'] = se
            d['ep'] = ep
            d['date'] = date
            cls.write(data)
            log.info(f'"{anime.lower()}" updated')
            return True
        
        data.append({'anime': anime.lower(), 'se': se, 'ep': ep,'date': date})
        cls.write(data)
        return True
                    
    @classmethod
    def show(cls, filter: str|None=None):
        log.info(f'filter by : "{filter}"')
        
        with open(cls.history_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            log.debug(f'{len(data)} data found from {cls.history_file}')
            
            cls.__print_history(data, filter)
        log.info(f'history showed successfully')

    @classmethod
    def __print_history(cls, data: list[dict], filter=None):
        """A pretty printer in table format to show the history

        Args:
            data (list[dict]): history data
            filter (str, optional): filter by an anime name. Defaults to None.
        """
        log.debug(f'{len(data)} data received')
        log.debug(f'filter by : "{filter}"')
        
        c1, c2, c3, c4 = 'Anime SE Ep Date'.split()
        line = lambda: print('+' + '~' * 73 + '+')
        
        line()
        print(f'|{c1:^15}|{c2:^15}|{c3:^15}|{c4:^25}|')
        line()

        for d in data:
            anime, se, ep, date = d.values()
            if filter is None:
                anime = anime[:cls.MAX_CHAR_SHOW]
                print(f'|{anime:^15}|{se:^15}|{ep:^15}|{date:^25}|')
                
            if filter is not None and anime == filter:
                anime = anime[:cls.MAX_CHAR_SHOW]
                print(f'|{anime:^15}|{se:^15}|{ep:^15}|{date:^25}|')
                log.info(f'filter by "{anime}" found.')
                
        line()
        log.debug(f'printed successfully')

    @classmethod
    def remove(cls, name: str) -> bool:
        """remove an anime from the history

        Args:
            name (str): anime name

        Returns:
            bool: True if removed successfully
        """
        if not os.path.isfile(cls.history_file):
            log.warning('history file not found')
            return
        
        data = cls.data()
        log.debug(f'{len(data)} found.')
        
        for index, dt in enumerate(data):
            anime = dt['anime'][:cls.MAX_CHAR_SHOW].lower()
            anm_to_rm = name[:cls.MAX_CHAR_SHOW].lower()
            
            if anime == anm_to_rm and cls.remove_confirmation(dt['anime']):
                data.pop(index)
                
                msg = f'\033[32mRemovido com sucesso.\033[m'
                log.info(msg)
                
                print(f'\033[33m{msg}\033[m')
                return True
        
        msg = f'\033[33m"{name}"\033[m não foi encontrado.'
        print(msg)
        log.debug(msg)
        return False
        
    @staticmethod
    def remove_confirmation(anm: str) -> bool:
        """get the confirmation to remove

        Args:
            anm (str): anime name to remove

        Returns:
            bool: True if removed successfully else False
        """
        confirm = input(
            f'\033[33mRemover "{anm}" do histórico? (s/n):\033[m '
        ).lower()
        resp = {'s': True, 'n': False}
        try:
            return resp[confirm]
        except KeyError:
            print('\033[31mOpção inválida!\033[m')
            log.warning('invalid option')
            return False
