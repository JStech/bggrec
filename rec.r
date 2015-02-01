library('Matrix')
library('lsa')

# cosine similarity function modified to ignore NA values
# probably terribly inefficient
na_cosine <- function(m) {
  c = matrix(0, nrow(m), nrow(m))
  for (i in 2:nrow(m)) {
    for (j in 1:i-1) {
      c[i,j] = cosine(na.omit(t(m[c(i, j),])))[1,2]
    }
  }
  c = c + t(c)
  diag(c) = 1
  return(c)
}

NUM_GAMES = 1000

# read in sparse matrix
x <- scan('matrix', what=list(integer(), integer(), numeric()))
M <- matrix(NA, max(x[[1]]), max(x[[2]]))
M[cbind(x[[1]], x[[2]])] <- x[[3]]

# take top NUM_GAMES games (by # of ratings)
topM = M[,1:NUM_GAMES]

# calculate user similarity
userSimilarity = na_cosine(topM)

#predictRatings <- function(user) {
#  weightedReviews = userSimilarity[,user] * topM[,-user]
#
#}
