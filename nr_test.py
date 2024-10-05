# import numpy as np
# from scipy.interpolate import lagrange
# import matplotlib.pyplot as plt
#
# # Define the data points
# x = np.array([0, 1, 2, 3])
# y = np.array([1, 2, 1, 0])
#
# # Create the Lagrange interpolating polynomial
# poly = lagrange(x, y)
#
# # Generate points for plotting the polynomial
# x_new = np.linspace(0, 3, 100)
# y_new = poly(x_new)
# #y = poly(x)
#
#
# # Plot the original data points and the interpolating polynomial
# plt.plot(x, y, 'o', label='Data points')
# plt.plot(x_new, y_new, label='Interpolated polynomial')
# plt.legend()
# plt.show()


import numpy as np
import random
import copy
import time
from scipy.interpolate import lagrange
import matplotlib.pyplot as plt

million = 10
l=list(range(10*million))
lr=copy.deepcopy(l)

start_time = time.time()
random.shuffle(lr)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.2f} seconds")


start_time = time.time()

# Define the data points
x = np.array(l)
y = np.array(lr)
#x = np.array([0, 1, 2])
#y = np.array([1, 3, 2])

# Create the Lagrange interpolating polynomial
poly = lagrange(x, y)

# Generate points for plotting the interpolation
x_new = np.linspace(0, max(l), 100)
y_new = poly(x_new)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Plot the original data points and the interpolation
plt.plot(x, y, 'o', label='Data Points')
plt.plot(x_new, y_new, label='Interpolation')
plt.legend()
#plt.show()