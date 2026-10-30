import numpy as np
from matplotlib import pyplot as plt

from plotting import plot_flow

size = 5           # half-width of the plotted domain
resolution = 1000  # grid points per axis
xs = np.linspace(-size, size, resolution)
ys = np.linspace(-size, size, resolution)
X, Y = np.meshgrid(xs, ys)
radius = 2         # cylinder radius R
v_free = 10        # free-stream velocity V_inf
k = radius**2 * v_free * 2 * np.pi  # doublet strength, chosen so the cylinder has radius R
delta = abs(xs[1] - xs[0])

uniform = lambda v, x, y: v * np.sqrt(x**2 + y**2) * np.sin(np.arctan2(y, x))
doublet = lambda k, x, y: - k * np.sin(np.arctan2(y, x)) / (np.sqrt(x**2 + y**2) * np.pi * 2)
pressure_coeff = lambda v, v_inf: 1 - (v / v_inf)**2

flow = uniform(v_free, X, Y) + doublet(k, X, Y)
mask = np.sqrt(X**2 + Y**2) < np.sqrt(k / (2 * np.pi * v_free))
flow[mask] = np.nan

u = np.gradient(flow, delta, axis=0)
v = -np.gradient(flow, delta, axis=1)
speed = np.sqrt(u**2 + v**2)

plot_flow(X, Y, flow, pressure_coeff(speed, v_free), radius,
          title="Nonlifting flow over a circular cylinder",
          filename="nonlifting_flow.png")
plt.show()
