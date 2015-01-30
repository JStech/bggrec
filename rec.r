library('Matrix')

x = scan('matrix', what=list(integer(), integer(), numeric()))
m = sparseMatrix(i=x[[1]], j=x[[2]], x=x[[3]])

