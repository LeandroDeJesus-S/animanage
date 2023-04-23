from datetime import datetime, timedelta
import logging as log
from pathlib import Path

from cli import features


class AutoUpdate:
    TIMEFILE = Path('autoupdate/.time').absolute()
    INTERVAL_DAYS = 3
    
    @classmethod
    def update(cls):
        with open(cls.TIMEFILE, 'r+') as f:
            last_up_time = datetime.fromtimestamp(float(f.readline()))
            log.debug(f'last update time : {last_up_time}')
            
            next_up_time = last_up_time + timedelta(days=cls.INTERVAL_DAYS)
            log.debug(f'next update time : {next_up_time}')
            
            now = datetime.now()
            log.debug(f'now time : {now}')
            
            if now >= next_up_time:
                features.CliFunctions().update()
                
                f.seek(0)
                f.write(f'{datetime.timestamp(now)}')
                log.info('time updated')
    
    @classmethod
    def do_update(cls):
        try:
            cls.update()
        except Exception as e:
            log.error(e)
