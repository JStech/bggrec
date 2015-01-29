#!/usr/bin/env python3

import bs4
import urllib3
from string import ascii_lowercase
from random import randint

USER_SEARCH = ('https://boardgamegeek.com/geeksearch.php?action=search&'+
        'objecttype=user&q={}&B1=Go')

# first, build a list of 10000 users who have rated at least 50 games
userList = []
urllib3.disable_warnings()
manager = urllib3.PoolManager()

while len(userList) < 10000:
    digraph = ''.join(ascii_lowercase[randint(0,25)] for i in range(2))
    html = manager.request('GET', USER_SEARCH.format(digraph)).data
    soup = bs4.BeautifulSoup(html, "lxml")
    user = soup.find("div", "username")
    print(user)
    exit()
