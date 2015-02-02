# bggrec
Building a board game recommendation engine using data from boardgamegeek.com.

*** Fair warning: this code got my IP blocked from boardgamegeek.com. Even
with just one request per second. ***

get_data.py downloads random users' review lists, and caches them (requires a
cached_users director)

make_matrix.py scans the cached_users directory and creates the matrix of
ratings in data.h5

train.r reads the matrix of ratings and calculates the cosine similarities for
all users, which also gets stored in data.h5

test.r calculates predicted ratings for a given user
