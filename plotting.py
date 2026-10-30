"""Shared plotting style for the potential-flow scripts."""

from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import Circle

FIGURE_DIR = Path(__file__).parent / "figures"

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "mathtext.fontset": "cm",
})


def plot_flow(X, Y, psi, cp, radius, title, filename, cp_min=-3.0, n_streamlines=41):
    """Plot the pressure coefficient field with streamlines and save it to figures/.

    Streamlines are drawn as contours of the stream function psi. The levels are
    equally spaced, so the same mass flow passes between neighbouring lines:
    where the lines bunch together, the flow is fast.

    The colour scale runs from cp_min to 1 (the stagnation value). The default of -3
    is the minimum on a nonlifting cylinder, so both plots share the same scale;
    lower values are clipped and marked by the arrow on the colour bar.
    """
    # Axes in units of the cylinder radius
    x, y = X / radius, Y / radius

    fig, ax = plt.subplots(figsize=(7.5, 5.8), layout="constrained")

    # Pressure coefficient on a linear colour scale
    field = ax.pcolormesh(x, y, cp, cmap="viridis", norm=Normalize(vmin=cp_min, vmax=1.0),
                          shading="auto", rasterized=True)
    clipped = np.nanmin(cp) < cp_min - 1e-3
    cbar = fig.colorbar(field, ax=ax, extend="min" if clipped else "neither", shrink=0.9)
    cbar.set_label(r"Pressure coefficient $C_p$")

    # Streamlines as equally spaced contours of psi
    levels = np.linspace(np.nanmin(psi), np.nanmax(psi), n_streamlines)
    ax.contour(x, y, psi, levels=levels, colors="white", linewidths=0.7,
               alpha=0.75, linestyles="solid")

    # The cylinder itself
    ax.add_patch(Circle((0, 0), 1.0, facecolor="0.8", edgecolor="0.1",
                        linewidth=1.2, zorder=3))

    # Free-stream direction
    x_min, x_max = x.min(), x.max()
    y_max = y.max()
    ax.annotate("", xy=(x_min + 0.16 * (x_max - x_min), 0.88 * y_max),
                xytext=(x_min + 0.04 * (x_max - x_min), 0.88 * y_max),
                arrowprops=dict(arrowstyle="-|>", color="0.1", lw=1.5), zorder=4)
    ax.text(x_min + 0.10 * (x_max - x_min), 0.80 * y_max, r"$V_\infty$",
            ha="center", va="top", fontsize=13, zorder=4,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.8))

    ax.set_aspect("equal")
    ax.set_xlabel(r"$x / R$")
    ax.set_ylabel(r"$y / R$")
    ax.set_title(title)

    FIGURE_DIR.mkdir(exist_ok=True)
    path = FIGURE_DIR / filename
    fig.savefig(path, dpi=200, bbox_inches="tight")
    print(f"Saved {path}")
    return fig, ax
