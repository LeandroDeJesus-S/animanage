from cli import arguments, features
from history import history

cli = features.CliFunctions()
if arguments.WATCH:
    cli.watch(arguments.WATCH, arguments.SEASON, arguments.EPISODE)
    history.WatchHistory.register(arguments.WATCH, 
                                  arguments.SEASON,
                                  arguments.EPISODE)

elif arguments.WATCHLATEST:
    cli.watch_latest(arguments.WATCHLATEST)

elif arguments.LIST_ANIME_RELEASES:
    cli.list_anime_release()

elif arguments.LIST_EP_RELEASES:
    cli.list_ep_release()

elif arguments.SEARCH:
    cli.search(arguments.SEARCH)

elif arguments.GETINFO:
    cli.get_info(arguments.GETINFO)

elif arguments.LISTEPS:
    cli.list_episodes(arguments.LISTEPS)    # TODO: how can i do this without infinite ifs?

elif arguments.CHANGENAME:
    cli.changename(arguments.CHANGENAME[0], arguments.CHANGENAME[1])

elif arguments.UPDATE:
    cli.update()

elif arguments.LISTSITES:
    cli.list_sites()

elif arguments.CHANGESITE:
    cli.change_site(arguments.CHANGESITE)

elif arguments.HISTORY and arguments.ADD_TO_HISTORY:
    name, se, ep = arguments.ADD_TO_HISTORY
    if isinstance(name, str) and se.isnumeric() and ep.isnumeric():
        history.WatchHistory.add(name, int(se), int(ep))
    else:
        print('Argumento inválido.')

elif arguments.HISTORY and arguments.REMOVE_FROM_HISTORY:
    history.WatchHistory.remove(arguments.REMOVE_FROM_HISTORY)
        
elif arguments.HISTORY:
    history.WatchHistory.show(filter=arguments.FILTERNAME)

elif arguments.ADD_ANIME:
    name, url = arguments.ADD_ANIME
    if not (isinstance(name, str) and isinstance(url, str)):
        print('Argumento inválido.')
    else:
        cli.add_anime(name, url)
