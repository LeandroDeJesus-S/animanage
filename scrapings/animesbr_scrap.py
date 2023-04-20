from pprint import pprint

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

except Exception as error:
	print(error)
import time

from requester.factory import Requesters
from parser.factory import Parsers
from animesbr.site import AnimesBr
from database.databases import SQLite

first_page = 'https://animesbr.cc/anime/'

req = Requesters.use_requests()
parser = Parsers.use_bs4()

first_page_content = req.get_content(first_page)

site = AnimesBr(parser, req)
db = SQLite()


titles = parser.select_all(first_page_content, 'div.title', text=True)
links = parser.select_all(first_page_content, 'div.data h3 a', attr='href')
data = [{'anime': a, 'link': l} for a, l in zip(titles, links)]

for page in range(2, 30):
	content = req.get_content(f'https://animesbr.cc/anime/page/{page}/')
	titles = parser.select_all(content, 'div.title', text=True)
	links = parser.select_all(content, 'div.data h3 a', attr='href')
	data += [{'anime': a, 'link': l} for a, l in zip(titles, links)]

db.connect('db.sqlite')

for d in data:
	anime, link = d.values()
	db.insert('animesbr_anime', ('anime', 'link'), (anime, link))

db.disconnect()
