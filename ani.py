from autoupdate.autoupdate import AutoUpdate
import logging as log

log.basicConfig(
    filename='logs.log', level=log.DEBUG, filemode='w', format='%(levelname)s - %(name)s - %(funcName)s - %(message)s'
)
# TODO: Colocar nomes melhores nas classes dos sites e melhorar os logs.


def main():
    from cli import main


if __name__ == '__main__':
    try:
        AutoUpdate.do_update()
        main()
    except Exception as exp:
        _ = log.error(exp), log.error(exp.__traceback__)
