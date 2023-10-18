from abc import ABC, abstractmethod
from typing import Any

from history.history import WatchHistory
from receivers import Anime, Releases, WebSites, History


class ICommand(ABC):
    @abstractmethod
    def execute(self): pass
    
    def log_command(self): pass
    
    
class WatchAnime(ICommand):
    def __init__(self,  anime: Anime, name: str, se=1, ep=1) -> None:
        self.anime = anime
        self.name = name
        self.season = se
        self.episode = ep
        
    def execute(self) -> None:
        self.anime.watch(self.name, self.season, self.episode)
    
    def log_command(self):
        WatchHistory.register(self.name, self.season, self.episode)
    
    
class WatchLatestEp(ICommand):
    def __init__(self,  anime: Anime, name: str) -> None:
        self.anime = anime
        self.name = name
        self.latest: tuple
        
    def execute(self) -> None:
        self.latest = self.anime.watch_latest(self.name)
    
    def log_command(self):
        if hasattr(self, 'latest'):
            WatchHistory.register(*self.latest)


class SearchAnime(ICommand):
    def __init__(self,  anime: Anime, name: str) -> None:
        self.anime = anime
        self.name = name
        
    def execute(self) -> None:
        self.anime.search(self.name)


class GetInfo(ICommand):
    def __init__(self,  anime: Anime, name: str) -> None:
        self.anime = anime
        self.name = name
        
    def execute(self) -> None:
        self.anime.get_info(self.name)


class ListEpisodes(ICommand):
    def __init__(self,  anime: Anime, name: str) -> None:
        self.anime = anime
        self.name = name
        
    def execute(self) -> None:
        self.anime.list_episodes(self.name)


class SetAlias(ICommand):
    def __init__(self, anime: Anime, name: str, alias: str) -> None:
        self.anime = anime
        self.name = name
        self.alias = alias
    
    def execute(self) -> None:
        self.anime.set_alias(self.alias, self.name)


class AddAnime(ICommand):
    def __init__(self, anime: Anime, name: str, url: str) -> None:
        self.anime = anime
        self.name = name
        self.url = url
    
    def execute(self) -> None:
        self.anime.add_anime(self.name, self.url)
    

class ListEpisodeReleases(ICommand):
    def __init__(self, releases: Releases) -> None:
        self.releases = releases
        
    def execute(self):
        self.releases.list_ep_releases()


class ListAnimeReleases(ICommand):
    def __init__(self, releases: Releases) -> None:
        self.releases = releases
        
    def execute(self):
        self.releases.list_anime_releases()


class UpdateReleases(ICommand):
    def __init__(self, releases: Releases) -> None:
        self.releases = releases
        
    def execute(self) -> None:
        self.releases.update()


class UpdateAllSitesReleases(ICommand):
    def __init__(self, releases: Releases) -> None:
        self.releases = releases
        
    def execute(self) -> None:
        self.releases.update_all_sites()


class ListSites(ICommand):
    def __init__(self, sites: WebSites):
        self.sites = sites
        
    def execute(self) -> None:
        self.sites.list_sites()
        

class ChangeSite(ICommand):
    def __init__(self, name, sites: WebSites):
        self.name = name
        self.sites = sites
        
    def execute(self):
        self.sites.change_site(self.name)


class ShowHistory(ICommand):
    def __init__(self, history: History):
        self.history = history
        
    def execute(self):
        self.history.show_history()
    

class AddToHistory(ICommand):
    def __init__(self, history: History, name: str, se: int, ep: int) -> None:
        self.history = history
        self.name = name
        self.se = se
        self.ep = ep

    def execute(self) -> None:
        self.history.add_to_history(self.name, self.se, self.ep)
    

class RemoveFromHistory(ICommand):
    def __init__(self, history: History, name: str) -> None:
        self.history = history
        self.name = name

    def execute(self) -> None:
        self.history.remove_from_history(self.name)
        

class ContinueByHistory(ICommand):
    def __init__(self, history: History, name: str) -> None:
        self.history = history
        self.name = name
    
    def execute(self):
        self.history.continue_by_history(self.name)


class Invoker:
    def __init__(self) -> None:
        self._commands: dict[Any, ICommand] = {}
    
    def add_command(self, key, command: ICommand):
        self._commands.update({key: command})
        
    def execute_command(self, key):
        self._commands[key].execute()
    
    def log_command(self, key):
        command = self._commands[key]
        if hasattr(command, 'log_command'):
            command.log_command()
