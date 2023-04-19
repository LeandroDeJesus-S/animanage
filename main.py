from anime.products import AnimesonlineSerie
from parser.factory import Parsers
from requester.factory import Requesters
from pprint import pprint

a = AnimesonlineSerie('https://animesonlinecc.to/anime/nanatsu-no-taizai-hd/',
                      Parsers.use_bs4(), Requesters.use_requests())

pprint(a.get_links())