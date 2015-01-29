#!/usr/bin/env python3

import bs4
import urllib3
import re
from string import ascii_lowercase
from random import randint

def userGen():
    USER_SEARCH = ('https://boardgamegeek.com/geeksearch.php?action=search&'+
            'objecttype=user&q={}&B1=Go')
    num_results_re = re.compile(r'Search Results \(([0-9]+) Matches?\)')
    user_re = re.compile(r'href="/user/([^"]+)"')

    urllib3.disable_warnings()
    manager = urllib3.PoolManager()

    used_tris = set()

    while True:
        # search on a random trigraph
        trigraph = ''.join(ascii_lowercase[randint(0,25)] for i in range(3))
        while trigraph in used_tris:
            trigraph = ''.join(ascii_lowercase[randint(0,25)] for i in range(3))
        used_tris.add(trigraph)
        html = manager.request('GET', USER_SEARCH.format(trigraph)).data

        soup = bs4.BeautifulSoup(html, "lxml")
        h2 = soup.find("h2")
        m = num_results_re.search(h2.decode())
        if m is None: continue
        num_results = int(m.group(1))
        for page in range(1, (num_results+99)//100 + 1):
            if page>1:
                html = manager.request('GET', USER_SEARCH.format(trigraph) +
                        '&pageID={}'.format(page))
                soup = bs4.BeautifulSoup(html, "lxml")
            users = soup.find_all("div", "username")
            for u in users:
                m = user_re.search(u.decode())
                if m is None: continue
                yield m.group(1)

for u in userGen():
    print(u)
