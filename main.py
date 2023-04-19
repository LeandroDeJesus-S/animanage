from anime.products import AnimesonlineSerie
from parser.factory import Parsers
from requester.factory import Requesters
from pprint import pprint
from release.ep.products import Animesonline

a = Animesonline(Parsers.use_bs4(), Requesters.use_requests())

pprint(a.get_releases())