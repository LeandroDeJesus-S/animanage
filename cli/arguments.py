import argparse

from cli import messages

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
    '-le', action='store_true', dest='list_ep_releases', 
    default=False, help=messages.le_msg
)

program.add_argument(
    '-la', action='store_true', dest='list_anime_releases',
    default=False, help=messages.la_msg
)

program.add_argument('--search', type=str, dest='search', 
                     metavar='<name>', help=messages.search_msg)
program.add_argument('--getinfo', type=str, dest='getinfo',
                     metavar='<name>', help=messages.getinfo_msg)
program.add_argument('--listeps', type=str, dest='listeps', 
                     metavar='<name>', help=messages.listeps_msg)

program.add_argument(
    '--changename', type=str, nargs=2, dest='changename',
    metavar=('<old_name>', '<new_name>'), help=messages.changename_msg
)

program.add_argument(
    '--update', action='store_true', dest='update',
    default=False, help=messages.update_msg
)

program.add_argument(
    '--listsites', action='store_true', dest='listsites',
    default=False, help=messages.listsites
)
program.add_argument(
    '--setsite', dest='setsite', type=str, 
    metavar='<site_name>', help=messages.setsite
)

program.add_argument(
    '--history', action='store_true', dest='history',
    default=False, help=messages.history_msg
)
program.add_argument(
    '-fn', '--filtername', type=str, dest='filtername', 
    metavar='<name>', help=messages.fn_msg
)
program.add_argument('--add', nargs=3,
                     metavar=('<name>', '<se>', '<ep>'), help=messages.add_msg)

args = program.parse_args()

HELPER = args.help

WATCH = args.watch
SEASON = args.season
EPISODE = args.episode

WATCHLATEST = args.watchlatest

LIST_ANIME_RELEASES = args.list_anime_releases
LIST_EP_RELEASES = args.list_ep_releases

SEARCH = args.search
GETINFO = args.getinfo
LISTEPS = args.listeps

CHANGENAME = args.changename

UPDATE = args.update

LISTSITES = args.listsites
SETSITE = args.setsite

HISTORY = args.history
FILTERNAME = args.filtername
ADD_TO_HISTORY = args.add
