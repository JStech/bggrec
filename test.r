library('rhdf5')

ratings <- t(h5read('data.h5', 'training_data/ratings'))
userSim <- h5read('data.h5', 'model/userSim')

numUsers <- nrow(userSim)

recommend <- function(user) {
  # weight ratings by user similarity
  weightedRatings = userSim[,user] * ratings
  # ignore user's own ratings (relevant to testing, irrelevant to actually
  # making recommendations--we won't recommend something they've already rated)
  weightedRatings = weightedRatings[-user,]

  # find weighted averages
  numerator = colSums(weightedRatings, na.rm = TRUE)
  # add an arbitrary smoothing constant, so we don't just recommend games that
  # one person rated 10/10
  denominator = colSums(userSim[-user,user] * (!is.na(weightedRatings))) + 5
  predictedRating = numerator / numRatings

  # build output
  numGames = length(predictedRating)
  game <- (1:numGames)[order(-predictedRating)]
  rating <- ratings[user,order(-predictedRating)]
  return(data.frame(game, predictedRating[order(-predictedRating)], rating))
}
