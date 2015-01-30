#!/usr/bin/env python3

import bs4
import glob
import sys
import os.path

users = []
games = dict()
next_game = 0

with open(sys.argv[1], "w") as output_file:
    for fn in glob.iglob('cached_users/*/*.xml'):
        with open(fn, "rb") as f:
            xml = f.read()
        if len(xml)==0: continue

        username = os.path.basename(fn)[:-4]
        users.append(username)
        userID = len(users)-1

        soup = bs4.BeautifulSoup(xml, "lxml")

        for gameSoup in soup.find_all("item"):
            bggID = int(gameSoup.get('objectid'))
            if bggID not in games:
                games[bggID] = next_game
                next_game += 1
            gameID = games[bggID]
            rating = gameSoup.findChild('rating').get('value')
            print(userID+1, gameID+1, rating, file=output_file)

with open(sys.argv[1]+'.users', "w") as output_file:
    for i, u in enumerate(users):
        print(i+1, u, file=output_file)

with open(sys.argv[1]+'.games', "w") as output_file:
    for bggID, gameID in games.items():
        print(gameID+1, bggID, file=output_file)
