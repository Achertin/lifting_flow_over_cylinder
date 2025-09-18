import numpy as np
from matplotlib import pyplot as plt

size = 15
resolution = 1000
xs = np.linspace(-size, size, resolution)
ys = np.linspace(-size, size, resolution)
X, Y = np.meshgrid(xs, ys)
radius = 2
v_inf = 30
delta = xs[1] - xs[0]
gamma = 1000

cylinder = lambda x, y: v_inf * np.sqrt(x**2 + y**2) * np.sin(np.arctan2(y, x)) * (1 - (radius / np.sqrt(x**2 + y**2))**2)
vortex = lambda x, y: gamma / (2 * np.pi) * np.log(np.sqrt(x**2 + y**2) / radius)
pressure_coeff = lambda v: 1 - (v / v_inf)**2

flow = cylinder(X, Y) + vortex(X, Y)
mask = np.sqrt(X**2 + Y**2) < radius
flow[mask] = np.nan

u = np.gradient(flow, delta, axis=0)
v = -np.gradient(flow, delta, axis=1)
speed = np.sqrt(u**2 + v**2)

plt.axes().set_aspect('equal')
plt.imshow(~mask, alpha=0.5, extent=(-size, size, -size, size), cmap='binary')
plt.pcolormesh(X, Y, pressure_coeff(speed), cmap='inferno')
plt.colorbar()
plt.streamplot(X, Y, u, v, density=2)
plt.show()
