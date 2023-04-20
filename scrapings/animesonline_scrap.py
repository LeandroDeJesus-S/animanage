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
from animesonline.site import Animesonline
from database.databases import SQLite

first_page = 'https://animesonlinecc.to/anime/'

req = Requesters.use_requests()
parser = Parsers.use_bs4()

site = Animesonline(parser, req)
db = SQLite()
site_anime_db = site.get_series_db(db)


data = []
for page in range(30, 81):
    content = req.get_content(f'https://animesonlinecc.to/anime/page/{page}/')
    titles = parser.select_all(content, 'div.data h3 a', text=True)
    links = parser.select_all(content, 'div.data h3 a', attr='href')
    data += [{'anime': a, 'link': l} for a, l in zip(titles, links)]

db.connect('db.sqlite')

site_anime_db.save_production(data)

db.disconnect()
