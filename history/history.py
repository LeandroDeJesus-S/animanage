import json
import os.path
from datetime import datetime
from locale import LC_ALL, setlocale
import logging as log
from pathlib import Path


class WatchHistory:
    HISTORY_FILE = Path('history/history.json').absolute()
    MAX_CHAR_SHOW = 15
    
    @classmethod
    def register(cls, w: str, s: int, e: int):
        loc = setlocale(LC_ALL, '')
        log.debug(f'locale : {loc}')
        
        file_exists = os.path.isfile(cls.HISTORY_FILE)
        log.debug(f'file exists : {file_exists}')
        if not file_exists:
            with open(cls.HISTORY_FILE, 'w+', encoding='utf-8') as f:
                json.dump([{'anime': w, 'se': s, 'ep': e}], f, indent=4, ensure_ascii=False)
                log.debug(f'"{cls.HISTORY_FILE}" was raised.')
        
        with open(cls.HISTORY_FILE, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            log.debug(f'history data found : {len(data)}')
            
            register_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
            for d in data:
                if d['anime'] != w.lower():
                    continue
                
                d['se'] = s
                d['ep'] = e
                d['date'] = register_date
                log.debug(f'updating "{w}" on {register_date}')
                break
            else:
                data.append({
                    'anime': w.lower(),
                    'se': s,
                    'ep': e,
                    'date': register_date
                })
                log.debug(f'"{w}" registered on {register_date}')
            
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            log.info(f'total data recorded : {len(data)}')
        return True
                        
    @classmethod
    def show(cls, filter=None):
        log.info(f'filter by : "{filter}"')
        
        with open(cls.HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            log.debug(f'{len(data)} data found from {cls.HISTORY_FILE}')
            
            cls.__print_history(data, filter)
        log.info(f'history showed successfully')

    @classmethod
    def __print_history(cls, data: list[dict], filter=None):
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
    def add(cls, name, se, ep):
        log.debug(f'adding : {name} se {se} ep {ep}')
        add = cls.register(name, se, ep)
        
        if add:
            log.info(f'"{name}" registered')
            return print(f'"{name}" adicionado ao histórico.')

        print(f'Falha ao adicionar "{name}" ao histórico!')
        log.warning(f'cannot add "{name}" to history.')

    @classmethod
    def remove(cls, name):
        if not os.path.isfile(cls.HISTORY_FILE):
            log.warning('history file not found')
            return
        
        with open(cls.HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            log.debug(f'{len(data)} found.')
        
        
        for i, d in enumerate(data):
            anime = d['anime']
            log.debug(f'anime: "{anime[:cls.MAX_CHAR_SHOW]}" | name: "{name[:cls.MAX_CHAR_SHOW]}"')
            if anime[:cls.MAX_CHAR_SHOW] != name[:cls.MAX_CHAR_SHOW].lower():
                continue
            
            log.debug(f'"{name}" found in history')
            confirm = input(f'\033[33mRemover "{d["anime"]}" do histórico? (s/n):\033[m ')
            log.debug(f'Confirmation answer : "{confirm}"')
            
            if confirm.lower() == 's':
                p = data.pop(i)
                log.debug(f'popped : {p}')
                with open(cls.HISTORY_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                msg = f'\033[32mRemovido com sucesso.\033[m'
                log.info(msg)
                
                print(f'\033[33m{msg}\033[m')
                
            elif confirm.lower() != 'n':
                print('Opção inválida.')
            break
        
        else:
            msg = f'"{name}" não foi encontrado.'
            print(msg)
            log.debug(msg)
                