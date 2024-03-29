from datetime import datetime
from locale import LC_ALL, setlocale
from pathlib import Path

import json
import logging as log
import os.path
import sys

class WatchHistory:
    MAX_CHAR_SHOW = 15
    history_file = Path(__file__).parent.absolute() / 'history.json'
    
    def __init__(self) -> None:
        self.create_file_if_not_exists()
    
    @classmethod
    def create_file_if_not_exists(cls):
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
        """register a new anime or update an existing anime in the history

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
        """Show the history table

        Args:
            filter (str | None, optional): anime name to filter. Defaults to None.
        """            
        log.info(f'filter by : "{filter}"')
        
        data = cls.data()
        log.debug(f'{len(data)} data found from {cls.history_file}')
        
        cls.__print_history(data, filter)
        log.info(f'history showed successfully')
    
    @classmethod
    def make_table(cls, data: list[dict]):
        """construct the table of the animes history"""
        c1, c2, c3, c4 = 'Anime SE Ep Date'.split()
        line = lambda: print('+' + '~' * 73 + '+')
        
        line()
        print(f'|{c1:^15}|{c2:^15}|{c3:^15}|{c4:^25}|')
        line()
        

        for d in data:
            anime, se, ep, date = d.values()
            anime = anime[:cls.MAX_CHAR_SHOW]
            
            print(f'|{anime:^15}|{se:^15}|{ep:^15}|{date:^25}|')
            line()
    
    @classmethod
    def __print_history_filter(cls, data: list[dict], filter: str):
        """Make the print just for the filtered results"""
        anm_filter = [d for d in data if filter.lower() in d['anime'].lower()]
        if not anm_filter:
            print('Nenhum resultado encontrado')
            return
        
        cls.make_table(anm_filter)

    @classmethod
    def __print_history(cls, data: list[dict], filter: str|None=None):
        """A pretty printer in table format to show the history

        Args:
            data (list[dict]): history data
            filter (str, optional): filter by an anime name. Defaults to None.
        """
        log.debug(f'{len(data)} data received')
        log.debug(f'filter by : "{filter}"')
        
        if filter is not None:
            cls.__print_history_filter(data, filter)
            return
        
        cls.make_table(data)
        log.debug(f'printed successfully')

    @staticmethod
    def remove_confirmation(anm: str) -> bool:
        """get the confirmation to remove

        Args:
            anm (str): anime name to remove

        Returns:
            bool: True if removed successfully else False
        """
        user_option = input(
            f'\033[33mRemover "{anm}" do histórico? (s/n):\033[m'
        ).lower()
        
        options = {'s': True, 'n': False}
        try:
            return options[user_option]
        except KeyError:
            print('\033[31mOpção inválida!\033[m')
            log.warning('invalid option')
            return False

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
            return False
        
        data = cls.data()
        log.debug(f'{len(data)} found.')
        
        for index, dt in enumerate(data):
            anime = dt['anime'][:cls.MAX_CHAR_SHOW].lower()
            anm_to_rm = name[:cls.MAX_CHAR_SHOW].lower()
            
            if anime == anm_to_rm and cls.remove_confirmation(dt['anime']):
                data.pop(index)
                
                msg = f'\033[32m"{anime}" Removido com sucesso.\033[m'
                log.info(msg)
                
                print(f'\033[33m{msg}\033[m')
                cls.write(data)
                return True
        
        msg = f'\033[33m"{name}"\033[m não foi encontrado.'
        print(msg)
        log.debug(msg)
        return False

    @classmethod
    def continue_by_history(cls, name: str):
        """redirect to next ep of the anime in the history"""
        py_cmd = 'python' if 'win' in sys.platform else 'python3'
            
        for register in cls.data():
            anime, se, ep, _ = register.values()

            if name.lower() == anime.lower():
                os.system(f'{py_cmd} ani.py -w "{anime}" -s {se} -e {ep + 1}')
                break
        
        else:
            print('\033[33mAnime não encontrado.\033[m')
