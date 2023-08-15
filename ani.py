from autoupdate.autoupdate import AutoUpdate
from colorama import init
import logging as log

log.basicConfig(
    filename='logs.log', level=log.DEBUG, filemode='w', 
    format='%(levelname)s - %(asctime)s - %(module)s > %(funcName)s > line %(lineno)d - %(message)s'
)


def main():
    from cli import main


if __name__ == '__main__':
    try:
        init()
        AutoUpdate.do_update()
        main()
    except Exception as exp:
        log.error(exp)
