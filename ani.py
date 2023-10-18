from autoupdate.autoupdate import AutoUpdate
from utils.decorators import try_exceptions
from colorama import init
import logging as log

log.basicConfig(
    filename='logs.log', level=log.DEBUG, filemode='w', 
    format='%(levelname)s - %(asctime)s - %(module)s > %(funcName)s > line %(lineno)d - %(message)s'
)

@try_exceptions(logger=log, log_type='error')
def main():
    from cli import main


if __name__ == '__main__':
    init()
    AutoUpdate.update()
    main()
