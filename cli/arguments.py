import argparse

program = argparse.ArgumentParser()

program.add_argument('-w', '--watch', type=str, dest='watch')
program.add_argument('-s', '--season', type=int, dest='season', default=1)
program.add_argument('-e', '--ep', type=int, dest='episode', default=1)


args = program.parse_args()

WATCH = args.watch
SEASON = args.season
EPISODE = args.episode

if WATCH:
    def watch(anime, se, ep):
        print(f'redirecting: {anime} se {se} ep {ep}')

    watch(WATCH, SEASON, EPISODE)
