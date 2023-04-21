from datetime import datetime, timedelta
import logging as log
from cli import features


class AutoUpdate:
    TIMEFILE = 'autoupdate/.time'
    INTERVAL_DAYS = 3
    
    @classmethod
    def do_update(cls):
        with open(cls.TIMEFILE, 'r+') as f:
            last_up_time = datetime.fromtimestamp(float(f.readline()))
            log.info(f'last update time : {last_up_time}')
            
            next_up_time = last_up_time + timedelta(days=cls.INTERVAL_DAYS)
            log.info(f'next update time : {next_up_time}')
            
            now = datetime.now()
            log.info(f'now time : {now}')
            
            if now >= next_up_time:
                features.CliFunctions().update()
                
                f.seek(0)
                f.write(f'{datetime.timestamp(now)}')
                log.info('time updated')

