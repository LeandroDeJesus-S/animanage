import json
from datetime import datetime
from locale import LC_ALL, setlocale
import logging as log


class WatchHistory:
    HISTORY_FILE = 'history/history.json'
    
    @classmethod
    def register(cls, w: str, s: int, e: int):
        setlocale(LC_ALL, 'pt_BR.utf-8')
        try:
            with open(cls.HISTORY_FILE, 'r+', encoding='utf-8') as f:
                data = json.load(f)
    
                log.debug(f'data : {data}')
                for d in data:
                    if d['anime'] != w.lower():
                        continue
                    
                    d['se'] = s
                    d['ep'] = e
                    break
                else:
                    data.append({
                        'anime': w.lower(),
                        'se': s,
                        'ep': e,
                        'date': str(datetime.now().strftime('%a, %d %b %Y %H:%M:%S'))
                    })

                log.info(f'dados finais: {data}')
                
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        
        except Exception as ex:
            _ = log.error(ex), log.error(ex.__traceback__)
            return False
                        
    @classmethod
    def show(cls, filter=None):
        with open(cls.HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cls.__print_history(data, filter)
            
    @staticmethod
    def __print_history(data: list[dict], filter=None):
        c1, c2, c3, c4 = 'Anime SE Ep Date'.split()
        line = lambda: print('+' + '~' * 73 + '+')
        
        line()
        print(f'|{c1:^15}|{c2:^15}|{c3:^15}|{c4:^25}|')
        line()
            
        
        for d in data:
            anime, se, ep, date = d.values()
            if filter is not None:
                if anime == filter:
                    print(f'|{anime[:15]:^15}|{se:^15}|{ep:^15}|{date:^25}|')
            else:
                print(f'|{anime[:15]:^15}|{se:^15}|{ep:^15}|{date:^25}|')
        line()

    @classmethod
    def add(cls, name, se, ep):
        add = cls.register(name, se, ep)
        if add:
            return print(f'"{name}" adicionado ao histórico.')

        print(f'Falha ao adicionar "{name}" ao histórico')
