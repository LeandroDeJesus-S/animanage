from cli import arguments
from history import history

if arguments.WATCH:
    arguments.invoker.execute_command('-w')

elif arguments.WATCHLATEST:
    arguments.invoker.execute_command('-wl')

elif arguments.LIST_ANIME_RELEASES:
    arguments.invoker.execute_command('-la')

elif arguments.LIST_EP_RELEASES:
    arguments.invoker.execute_command('-le')

elif arguments.SEARCH:
    arguments.invoker.execute_command('--search')

elif arguments.GETINFO:
    arguments.invoker.execute_command('--getinfo')

elif arguments.LISTEPS:
    arguments.invoker.execute_command('--listeps')

elif arguments.SETALIAS and arguments.SETALIAS[0] is not None:
    arguments.invoker.execute_command('--alias')

elif arguments.UPDATE and arguments.UPDATE_ALL:
    arguments.invoker.execute_command('--update --all')

elif arguments.UPDATE:
    arguments.invoker.execute_command('--update')

elif arguments.LISTSITES:
    arguments.invoker.execute_command('--listsites')

elif arguments.CHANGESITE:
    arguments.invoker.execute_command('--changesite')

elif arguments.HISTORY:
    if arguments.ADD_TO_HISTORY and arguments.ADD_TO_HISTORY[0] is not None:
        arguments.invoker.execute_command('--history --add')
    
    elif arguments.REMOVE_FROM_HISTORY:
        arguments.invoker.execute_command('--history --remove')

    else:
        arguments.invoker.execute_command('--history')

elif arguments.ADD_ANIME and arguments.ADD_ANIME[0] is not None:
    arguments.invoker.execute_command('--add-anime')
