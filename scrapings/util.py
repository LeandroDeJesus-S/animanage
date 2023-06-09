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


def scrap(qTitle, qLinks, first_page, endpoint, pRange, parser, requester, dbEng, dbOrigin):
    """make the scraping to extract anime data.

    Args:
        qTitle (str): html query to get the title of the anime.
        qLinks (str): css query to get anime links.
        first_page (str): first url to start the scraping
        endpoint (str): end point of the other pages when are the animes.
        pRange (tuple): range of pages to do the scraping.
        parser (ParserObj): instance of a parser object.
        requester (RequesterObj): instance of a requester object
        dbEng (DbObj): instance of the db engine class
        dbOrigin (DbObj): instance of the anime db
    """
    data = []
    for page in range(1, pRange):
        link = first_page + endpoint.format(page)
        if page == 1:
            link = first_page
            
        content = requester.get_content(link)
        titles = parser.select_all(content, qTitle, text=True)
        links = parser.select_all(content, qLinks, attr='href')
        data += [{'anime': a, 'link': l} for a, l in zip(titles, links)]

    dbEng.connect('db.sqlite')

    dbOrigin.save_production(data)

    dbEng.disconnect()


if __name__ == '__main__':
    first_page = 'https://animesonlinecc.to/anime/'
    endpoint = 'page/{}/'
    parser = Parsers.use_bs4()
    req = Requesters.use_requests()

    db = SQLite()
    site = Animesonline(parser, req, db)
    site_anime_db = site.get_series_db()
    scrap(
        'div.data h3 a', 'div.data h3 a', first_page, 
        endpoint, parser,req, db, site_anime_db, pRange=(1,11)
    )
