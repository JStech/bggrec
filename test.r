library('rhdf5')

ratings <- t(h5read('data.h5', 'training_data/ratings'))
userSim <- h5read('data.h5', 'model/userSim')

numUsers <- nrow(userSim)

recommend <- function(user) {
  weightedRatings = userSim[,user] * ratings
  gameSums = colSums(weightedRatings, na.rm = TRUE)
  # arbitrary smoothing constant
  numRatings = colSums(!is.na(weightedRatings)) + 5
  predictedRating = gameSums / numRatings
  numGames = length(predictedRating)
  game <- 1:numGames
  rating <- ratings[user,]
  return(data.frame(game, predictedRating, rating))
}
