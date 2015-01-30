#!/usr/bin/env python3

import bs4
import os
import glob
import os.path
import re
import time
import urllib
import urllib3
from string import ascii_lowercase
from random import randint

urllib3.disable_warnings()
manager = urllib3.PoolManager()

def userGen():
    USER_SEARCH = ('https://boardgamegeek.com/geeksearch.php?action=search&'+
            'objecttype=user&q={}&B1=Go')
    num_results_re = re.compile(r'Search Results \(([0-9]+) Matches?\)')
    user_re = re.compile(r'href="/user/([^"]+)"')

    used_tris = set()

    while True:
        # search on a random trigraph
        while True:
            trigraph = ''.join(ascii_lowercase[randint(0,25)] for i in range(3))
            if trigraph not in used_tris: break
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

def getUserRatings(user):
    escaped_user = user.translate(str.maketrans(r'/\?%*:|"<>', '__________'))
    userdir = 'cached_users/'+escaped_user[:2]
    userfile = userdir+'/'+escaped_user+'.xml'
    if not os.path.isfile(userfile):
        collection_url = 'http://www.boardgamegeek.com/xmlapi/collection/{}?rated=1'
        while True:
            html = manager.request('GET', collection_url.format(urllib.parse.quote(user)))
            if html.status != 202: break
            time.sleep(0.7)
        if html.status != 200:
            print("dying on", collection_url.format(urllib.parse.quote(user)))
            exit()
        if not os.path.isdir(userdir):
            os.mkdir(userdir)
        items = bs4.BeautifulSoup(html.data).find('items')
        games = 0
        if items is not None: games = int(items.get('totalitems'))
        f = open(userfile, 'wb')
        if games>0: f.write(html.data)
        f.close()
        return games
    with open(userfile, 'rb') as f:
        d = f.read()
    if len(d)==0: return 0
    return int(bs4.BeautifulSoup(d).find('items').get('totalitems'))

ten_games = 0

for userfile in glob.iglob('./cached_users/*/*.xml'):
    with open(userfile, 'rb') as f:
        d = f.read()
    if len(d)==0: continue
    if int(bs4.BeautifulSoup(d).find('items').get('totalitems'))>10:
        ten_games += 1

for u in userGen():
    print('getting', u)
    g = getUserRatings(u)
    time.sleep(0.2 + randint(0,10)/10)
    print('got', u, g, ten_games)
    if g>10:
        ten_games += 1
        if ten_games >= 2000: break
