import argparse

from cli import messages, commands

program = argparse.ArgumentParser(usage=messages.USAGE)


program.add_argument(
    '-w', '--watch', type=str, dest='watch', 
    metavar='<name>', help=messages.w_msg
)
program.add_argument(
    '-s', '--season', type=int, dest='season',
    default=1, metavar='<n>', help=messages.s_msg
)
program.add_argument(
    '-e', '--ep', type=int, dest='episode', 
    default=1, metavar='<n>', help=messages.e_msg
)
program.add_argument(
    '-wl', '--watchlatest', type=str, dest='watchlatest', 
    metavar='<name>', help=messages.wl_msg
)

program.add_argument(
    '-le', '--listep-release', action='store_true', dest='list_ep_releases', 
    default=False, help=messages.le_msg
)
program.add_argument(
    '-la', '--listanime-release', action='store_true', dest='list_anime_releases',
    default=False, help=messages.la_msg
)

program.add_argument('--search', type=str, dest='search', 
                     metavar='<name>', help=messages.search_msg)
program.add_argument('--getinfo', '-i', type=str, dest='getinfo',
                     metavar='<name>', help=messages.getinfo_msg)
program.add_argument('--listeps', type=str, dest='listeps', 
                     metavar='<name>', help=messages.listeps_msg)

program.add_argument(
    '--alias', type=str, nargs=2, dest='set_alias',
    metavar=('<old_name>', '<new_name>'),
    help=messages.alias_msg, default=[None, None]
)

program.add_argument(
    '--update', '-up', action='store_true', dest='update',
    default=False, help=messages.update_msg
)
program.add_argument(
    '--all', '-a', action='store_true', dest='up_all',
    default=False, help=messages.update_all_msg
)

program.add_argument(
    '--listsites', action='store_true', dest='listsites',
    default=False, help=messages.listsites_msg
)
program.add_argument(
    '--changesite', dest='changesite', type=str, 
    metavar='<site_name>', help=messages.changesite_msg
)

program.add_argument(
    '--history', '-H', action='store_true', dest='history',
    default=False, help=messages.history_msg
)

program.add_argument(
    '--continue', '-c', type=str, dest='continue_history',
    default='', help=messages.continue_hist_msg
)

program.add_argument(
    '-fn', '--filtername', type=str, dest='filtername', 
    metavar='<name>', help=messages.fn_msg
)
program.add_argument(
    '--add', nargs=3, metavar=('<name>', '<se>', '<ep>'),
    help=messages.add_msg, default=[None, None, None]
)
program.add_argument(
    '-r', '--remove', type=str, dest='remove', help=messages.remove_msg
)
program.add_argument(
    '--add-anime', nargs=2, dest='add_anime',
    metavar=('<name>', '<url>'), 
    help=messages.add_anime_msg, default=[None, None]
)

args = program.parse_args()

WATCH = args.watch
SEASON = args.season
EPISODE = args.episode

WATCHLATEST = args.watchlatest

LIST_ANIME_RELEASES = args.list_anime_releases
LIST_EP_RELEASES = args.list_ep_releases

SEARCH = args.search
GETINFO = args.getinfo
LISTEPS = args.listeps

SETALIAS = args.set_alias

UPDATE = args.update
UPDATE_ALL = args.up_all

LISTSITES = args.listsites
CHANGESITE = args.changesite

HISTORY = args.history
CONTINUE_HISTORY = args.continue_history
FILTERNAME = args.filtername
ADD_TO_HISTORY = args.add
REMOVE_FROM_HISTORY = args.remove

ADD_ANIME = args.add_anime

anime = commands.Anime()

watch_cmd = commands.WatchAnime(anime, WATCH, SEASON, EPISODE)
watch_latest_cmd = commands.WatchLatestEp(anime, WATCHLATEST)
search_cmd = commands.SearchAnime(anime, SEARCH)
get_info_cmd = commands.GetInfo(anime, GETINFO)
list_episodes_cmd = commands.ListEpisodes(anime, LISTEPS)
set_alias_cmd = commands.SetAlias(anime, SETALIAS[0], SETALIAS[1])
add_anime_cmd = commands.AddAnime(anime, ADD_ANIME[0], ADD_ANIME[1])

releases = commands.Releases()

list_episode_releases_cmd = commands.ListEpisodeReleases(releases)
list_anime_releases_cmd = commands.ListAnimeReleases(releases)

update_releases_cmd = commands.UpdateReleases(releases)
update_all_sites_releases_cmd = commands.UpdateAllSitesReleases(releases)

sites = commands.WebSites()

ch_site = commands.ChangeSite(CHANGESITE, sites)
ls_sites = commands.ListSites(sites)

history = commands.History(FILTERNAME)

continue_by_history_cmd = commands.ContinueByHistory(history, CONTINUE_HISTORY)
show_history_cmd = commands.ShowHistory(history)
add_to_history_cmd = commands.AddToHistory(
    history, ADD_TO_HISTORY[0], ADD_TO_HISTORY[1], ADD_TO_HISTORY[2]
)
remove_from_history_cmd = commands.RemoveFromHistory(history, REMOVE_FROM_HISTORY)

invoker = commands.Invoker()

invoker.add_command('-w', watch_cmd)
invoker.add_command('-wl', watch_latest_cmd)
invoker.add_command('--search', search_cmd)
invoker.add_command('--getinfo', get_info_cmd)
invoker.add_command('--listeps', list_episodes_cmd)
invoker.add_command('--alias', set_alias_cmd)
invoker.add_command('--add-anime', add_anime_cmd)

invoker.add_command('-le', list_episode_releases_cmd)
invoker.add_command('-la', list_anime_releases_cmd)

invoker.add_command('--update', update_releases_cmd)
invoker.add_command('--update --all', update_all_sites_releases_cmd)

invoker.add_command('--listsites', ls_sites)
invoker.add_command('--changesite', ch_site)

invoker.add_command('--history', show_history_cmd)
invoker.add_command('--history --continue', continue_by_history_cmd)
invoker.add_command('--history --add', add_to_history_cmd)
invoker.add_command('--history --remove', remove_from_history_cmd)
