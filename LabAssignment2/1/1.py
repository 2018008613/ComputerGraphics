import numpy as np

#A.

M = np.arange(2,27,1)
print(M)

#B.

M = M.reshape(5,5)
print(M)

#C.

M[1:4,1:4] = 0
print(M)

#D.

M = M @ M
print(M)

#E.

v = M[0,0:]
print(np.sqrt(v @ v))
