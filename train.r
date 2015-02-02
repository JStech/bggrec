library('Matrix')
library('lsa')
library('rhdf5')

# cosine similarity function modified to ignore NA values
# probably terribly inefficient
na_cosine <- function(m) {
  c = matrix(0, nrow(m), nrow(m))
  for (i in 2:nrow(m)) {
    if (i%%100 == 0) {cat(i, '\n')}
    for (j in 1:(i-1)) {
      c[i,j] = cosine(na.omit(cbind(m[i,], m[j,])))[1,2]
    }
  }
  c = c + t(c)
  diag(c) = 1
  return(c)
}

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
