from autoupdate.autoupdate import AutoUpdate
import logging as log

log.basicConfig(
    filename='logs.log', level=log.DEBUG, filemode='w', format='%(levelname)s - %(name)s - %(funcName)s - %(message)s'
)

def main():
    from cli import main


if __name__ == '__main__':
    AutoUpdate.do_update()
    main()