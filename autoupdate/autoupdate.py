from datetime import datetime, timedelta
import logging as log
from pathlib import Path

from cli import command, arguments


class AutoUpdate:
    TIMEFILE = Path('autoupdate/.time').absolute()
    INTERVAL_DAYS = 3
    
    def __init__(self) -> None:
        self.verify_file_exists()
    
    @classmethod
    def verify_file_exists(cls):
        if not cls.TIMEFILE.exists():
            cls.TIMEFILE.touch()
    
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
                arguments.invoker.execute_command('--update')
                
                f.seek(0)
                f.write(f'{datetime.timestamp(now)}')
                log.info('time updated')
    
    @classmethod
    def do_update(cls):
        try:
            cls.update()
        except Exception as e:
            log.error(e)
