library('Matrix')
library('lsa')
library('rhdf5')

source('na_cosine.r')

NUM_GAMES = 1000

# read in sparse matrix
M <- t(h5read('data.h5', 'training_data/ratings'))
M[is.nan(M)] <- NA

# take top NUM_GAMES games (by # of ratings)
topM = M[,1:NUM_GAMES]

# calculate user similarity
userSimilarity = na_cosine(topM)

h5createGroup('data.h5', 'model')
h5write(userSimilarity, 'data.h5', 'model/userSim')
