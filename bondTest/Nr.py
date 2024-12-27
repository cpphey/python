import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt

# Original array of numbers between 0 and 1 (dummy data)
x = np.linspace(0, 1, 10)  # Original x values
y = np.random.rand(10)     # Random y values between 0 and 1

# Create a finer grid
x_fine = np.linspace(0, 1, 100)

# Create a spline interpolator (cubic spline)
spline = make_interp_spline(x, y, k=3)

# Evaluate the spline at the finer grid
y_smooth = spline(x_fine)

# Plot the results (optional)
plt.figure(figsize=(8, 4))
plt.plot(x, y, 'o', label="Original Points (Dummy Data)")
plt.plot(x_fine, y_smooth, '-', label="Spline Interpolation")
plt.legend()
plt.title("Spline Interpolation with Dummy Data")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.show()
