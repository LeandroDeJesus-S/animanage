from pprint import pprint

from requester.factory import Requesters
from parser.factory import Parsers

first_page = 'https://animesbr.cc/anime/'

other_pages = 'https://animesbr.cc/anime/page/{num}'

req = Requesters.use_requests()
parser = Parsers.use_bs4()


content = req.get_content(first_page)
result = parser.select_all(content, 'div.animation-1', text=True)
pprint(result)