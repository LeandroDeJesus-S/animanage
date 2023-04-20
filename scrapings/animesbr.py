try:
	import sys
	import os

	sys.path.append(
		os.path.abspath(
			os.path.join(
				os.path.dirname(__file__), '..'
			)
		)
	)

except:
	pass

from pprint import pprint

from requester.factory import Requesters
from parser.factory import Parsers
from animesbr.animesbr import AnimesBr

first_page = 'https://animesbr.cc/anime/'

other_pages = 'https://animesbr.cc/anime/page/{num}'

req = Requesters.use_requests()
parser = Parsers.use_bs4()


content = req.get_content(first_page)

titles = parser.select_all(content, 'div.title', text=True)
links = parser.select_all(content, 'div.data h3 a', attr='href')


for t, l in zip(titles, links):
	print(t, l)