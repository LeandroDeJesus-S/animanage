import products
import requests
from parser.products import Bs4Parser, ParselParser
from requester.factory import Requesters
from parsel import Selector
from bs4 import BeautifulSoup

from pprint import pprint

link = 'https://animesonlinecc.to/anime/vinland-saga/'
link = 'https://animesonlinecc.to/anime/nanatsu-no-taizai-hd/'
