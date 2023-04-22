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
import logging as log
log.basicConfig(
    filename='logs.log', level=log.DEBUG, filemode='w', format='%(levelname)s - %(name)s - %(funcName)s - %(message)s'
)
from requester.factory import Requesters
from parser.factory import Parsers
from animesonline_online.site import AnimesonlineOnline
from database.databases import SQLite

first_page = 'https://animesonlinecc.to/anime/'

req = Requesters.use_requests()
parser = Parsers.use_bs4()

site = AnimesonlineOnline(parser, req)
db = SQLite()
site_anime_db = site.get_series_db(db)

data = []
for page in range(2, 80):
    time.sleep(.2)
    content = req.get_content(f'https://ww31.animesonline.online/animes/page/{page}/', type='text')
    animes = parser.select_all(content, 'div.animation-2 article.item div.data h3 a')
    titles = [a.text for a in animes]
    links = [a.get('href') for a in animes]
    data += [{'anime': a, 'link': l} for a, l in zip(titles, links)]
# pprint(data)
#
db.connect('../db.sqlite')
#
site_anime_db.save_production(data)
#
db.disconnect()
