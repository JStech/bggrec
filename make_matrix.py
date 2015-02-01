#!/usr/bin/env python3

import bs4
import glob
import h5py
import numpy as np
import sys
import os.path

users = []
games = dict()
next_game = 0
ratings = dict()

print("reading data")
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
            games[bggID] = 0
        games[bggID] += 1
        rating = gameSoup.findChild('rating').get('value')
        ratings[userID, bggID] = float(rating)

print("done reading data")

numUsers = len(users)
maxUsernameLen = max(len(n) for n in users)

# assign game IDs in decreasing order of number of reviews
gameIDs = dict()
next_gameID = 0
for bggID, _ in sorted(games.items(), key=lambda x: x[1], reverse=True):
    gameIDs[bggID] = next_gameID
    next_gameID += 1

numGames = len(games)

with h5py.File("data.h5") as f:
    if 'training_data/ratings' in f:
        del f['training_data/ratings']
    print("writing data--ratings")
    f.create_dataset('training_data/ratings', (numUsers, numGames), dtype='f')
    # use NaN for missing data
    f['training_data/ratings'][:] = float('NaN')
    for (userID, bggID), rating in ratings.items():
        f['training_data/ratings'][userID, gameIDs[bggID]] = rating

    print("writing data--users")
    if 'training_data/users' in f:
        del f['training_data/users']
    f.create_dataset('training_data/users', (numUsers,),
            dtype='a'+str(maxUsernameLen))
    for i, u in enumerate(users):
        f['training_data/users'][i] = u.encode()

    print("writing data--games")
    if 'training_data/games' in f:
        del f['training_data/games']
    f.create_dataset('training_data/games', (numGames,),
            dtype='i')
    for bggID, gameID in games.items():
        f['training_data/games'][gameID] = bggID
