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

