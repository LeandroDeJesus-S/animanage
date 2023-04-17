import products
import requests
from bs4 import BeautifulSoup
import pprint
link = 'https://animesonlinecc.to/anime/vinland-saga/'
link = 'https://animesonlinecc.to/anime/nanatsu-no-taizai-hd/'
anime = products.AnimesonlineSerie(link, parsers=BeautifulSoup, requesters=requests)

rate = anime.get_evaluation_points()
print('rate:', rate)

categories = anime.get_category()
print('categories:', categories)
sinopse = anime.get_sinopse()
print('\nsinopse:', sinopse)
print('last season:', anime.last_season)
print('last episode:', anime.last_ep)
# pprint.pprint(anime.get_links())


