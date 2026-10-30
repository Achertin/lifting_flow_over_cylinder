import numpy as np
from matplotlib import pyplot as plt

from plotting import plot_flow

size = 15          # half-width of the plotted domain
resolution = 1000  # grid points per axis
xs = np.linspace(-size, size, resolution)
ys = np.linspace(-size, size, resolution)
X, Y = np.meshgrid(xs, ys)
radius = 2         # cylinder radius R
v_inf = 30         # free-stream velocity V_inf
delta = xs[1] - xs[0]
gamma = 1000       # circulation Gamma (positive = clockwise)

cylinder = lambda x, y: v_inf * np.sqrt(x**2 + y**2) * np.sin(np.arctan2(y, x)) * (1 - (radius / np.sqrt(x**2 + y**2))**2)
vortex = lambda x, y: gamma / (2 * np.pi) * np.log(np.sqrt(x**2 + y**2) / radius)
pressure_coeff = lambda v: 1 - (v / v_inf)**2

flow = cylinder(X, Y) + vortex(X, Y)
mask = np.sqrt(X**2 + Y**2) < radius
flow[mask] = np.nan

u = np.gradient(flow, delta, axis=0)
v = -np.gradient(flow, delta, axis=1)
speed = np.sqrt(u**2 + v**2)

ratio = gamma / (4 * np.pi * v_inf * radius)
plot_flow(X, Y, flow, pressure_coeff(speed), radius,
          title=rf"Lifting flow over a circular cylinder, $\Gamma / (4\pi V_\infty R) = {ratio:.2f}$",
          filename="lifting_flow.png")
plt.show()
