import numpy as np

from src.SimplexSolver import SimplexSolver

from src.server import app

# A = np.array([[1, 2, 1, 0], [3, 1, 0, 1]])
# c_T = np.array([-1, -1, 0, 0])
# b = np.array([[2], [3/2]])
#
# s = SimplexSolver(A, b, c_T, (0, 0))
# print(s.indexes_base)
# print(s.indexes_non_base)
# s.solve()

# A = np.array([[1, 4, 1, 0, 0], [14, 4, 0, 1, 0], [1, 0, 0, 0, 1]])
# c_T = np.array([-4, -3, 0, 0, 0])
# b = np.array([[52], [156], [10]])
#
# s = SimplexSolver(A, b, c_T, (0, 0))

# print(s.indexes_base)
# print(s.indexes_non_base)
# print(s.values)
#
# print(s.get_c_T_base())
# print(s.get_c_T_non_base())

# s.solve()

app.run()