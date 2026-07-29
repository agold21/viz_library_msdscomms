"""Shared color and styling helpers for the visualizer_alex plots.

Every plot in this library shares one visual language:

* a **blue -> green** encoding keyed to the median -- marks below the median
  trend blue, marks above trend green, and the further from the median the
  more saturated the color becomes; and
* a professional dark theme -- black background, white text, a clean
  sans-serif font, bold titles, and white outlines.

This module is the single source of truth for both, so ``histogram``,
``heatmap``, and ``scatterplot`` stay consistent.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

# Endpoint colors of the blue -> green spectrum.
_BLUE = (0.10, 0.25, 0.75)
_GREEN = (0.15, 0.70, 0.35)

# Preferred sans-serif families, in order, for a clean professional look.
# Registered ahead of matplotlib's defaults so plots use them when installed
# and fall back silently to DejaVu Sans (always available) otherwise.
_PREFERRED_FONTS = ["Helvetica", "Arial", "Helvetica Neue", "DejaVu Sans"]


def blend(weight: float) -> tuple[float, float, float]:
    """Linearly interpolate from blue (weight=0) to green (weight=1)."""
    return tuple(b + weight * (g - b) for b, g in zip(_BLUE, _GREEN))


def bluegreen_cmap(name: str = "bluegreen") -> LinearSegmentedColormap:
    """Return a continuous blue -> green colormap (for heatmaps, colorbars)."""
    return LinearSegmentedColormap.from_list(name, [_BLUE, blend(0.5), _GREEN])


def use_preferred_fonts() -> None:
    """Prefer professional sans-serif fonts, falling back silently to defaults."""
    existing = [f for f in plt.rcParams["font.sans-serif"] if f not in _PREFERRED_FONTS]
    plt.rcParams["font.sans-serif"] = _PREFERRED_FONTS + existing


def median_norm(values, median: float) -> Normalize:
    """A Normalize centered on the median, symmetric to the farthest value.

    Mapping the median to 0.5 (teal) with the most-distant value reaching 0 or
    1 makes the blue and green extremes saturate at the same distance on either
    side -- the same scaling the histogram uses.
    """
    max_dist = max((abs(v - median) for v in values), default=0.0) or 1.0
    return Normalize(vmin=median - max_dist, vmax=median + max_dist)


def median_weights(values, median: float) -> list[float]:
    """Map each value to a blue->green weight in [0, 1] by distance from median."""
    norm = median_norm(values, median)
    return [float(norm(v)) for v in values]


def apply_dark_style(ax, title=None, xlabel=None, ylabel=None) -> None:
    """Apply the shared dark theme (black background, white text) to ``ax``."""
    ax.figure.set_facecolor("black")
    ax.set_facecolor("black")

    if title is not None:
        ax.set_title(
            title, color="white", fontweight="bold", fontsize=14, fontfamily="sans-serif"
        )
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    # Recolor whatever axis labels exist (including seaborn's auto labels).
    ax.xaxis.label.set_color("white")
    ax.xaxis.label.set_fontfamily("sans-serif")
    ax.yaxis.label.set_color("white")
    ax.yaxis.label.set_fontfamily("sans-serif")

    ax.tick_params(colors="white")
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontfamily("sans-serif")
    for spine in ax.spines.values():
        spine.set_color("white")


def style_colorbar_white(cbar) -> None:
    """Style a colorbar for the dark theme: white ticks, labels, and outline."""
    cbar.ax.tick_params(colors="white")
    for label in cbar.ax.get_yticklabels():
        label.set_fontfamily("sans-serif")
    cbar.ax.yaxis.label.set_color("white")
    cbar.ax.yaxis.label.set_fontfamily("sans-serif")
    if cbar.outline is not None:
        cbar.outline.set_edgecolor("white")


def add_bluegreen_colorbar(ax, values, median: float, label: str | None = None):
    """Add a blue->green colorbar keyed to the median, explaining the encoding.

    Uses the same median-centered normalization as :func:`median_weights`, so
    the colorbar matches the colors of the marks it describes.
    """
    sm = plt.cm.ScalarMappable(cmap=bluegreen_cmap(), norm=median_norm(values, median))
    sm.set_array([])
    cbar = ax.figure.colorbar(sm, ax=ax)
    if label:
        cbar.set_label(label)
    style_colorbar_white(cbar)
    return cbar
