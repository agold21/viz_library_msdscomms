"""Core functionality for the visualizer library."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Endpoint colors of the blue -> green spectrum.
# Bars far below the median trend toward BLUE; bars far above trend toward GREEN.
_BLUE = (0.10, 0.25, 0.75)
_GREEN = (0.15, 0.70, 0.35)

# Preferred sans-serif families, in order, for a clean professional look.
# These are registered ahead of matplotlib's defaults so the plot uses them
# when installed and falls back silently to DejaVu Sans (always available)
# otherwise. Text elements reference the generic "sans-serif" family, which
# resolves through this list without emitting missing-font warnings.
_PREFERRED_FONTS = ["Helvetica", "Arial", "Helvetica Neue", "DejaVu Sans"]


def _blend(weight: float) -> tuple[float, float, float]:
    """Linearly interpolate from blue (weight=0) to green (weight=1)."""
    return tuple(b + weight * (g - b) for b, g in zip(_BLUE, _GREEN))


def histogram(data, bins: int = 10, title: str = "Histogram", ax=None, **hist_kwargs):
    """Plot a professionally styled histogram colored by position vs. the median.

    The histogram is drawn with :func:`seaborn.histplot`. Bars whose center
    falls below the median are shaded toward blue, and bars above the median
    toward green. The further a bar sits from the median, the more saturated
    its color becomes in the respective direction.

    The figure uses a black background with white text, a professional
    sans-serif font, a bold title, and white bar outlines.

    Parameters
    ----------
    data : array-like or pandas.Series
        The values to histogram. Missing values (NaN) are dropped.
    bins : int, default 10
        Number of histogram bins passed through to ``seaborn.histplot``.
    title : str, default "Histogram"
        Bold title rendered at the top of the plot.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. If omitted, a new figure and axes are created.
    **hist_kwargs
        Additional keyword arguments forwarded to ``seaborn.histplot``. An
        ``edgecolor`` supplied here overrides the default white bar outline.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the styled, colored histogram.
    """
    series = pd.Series(data).dropna()
    if series.empty:
        raise ValueError("`data` contains no non-null values to plot.")

    median = series.median()

    # Prefer professional sans-serif fonts, falling back silently to defaults.
    existing = [f for f in plt.rcParams["font.sans-serif"] if f not in _PREFERRED_FONTS]
    plt.rcParams["font.sans-serif"] = _PREFERRED_FONTS + existing

    if ax is None:
        _, ax = plt.subplots()

    # Black background for both the figure and the plotting area.
    ax.figure.set_facecolor("black")
    ax.set_facecolor("black")

    # White bar outlines by default (still overridable via hist_kwargs).
    hist_kwargs.setdefault("edgecolor", "white")
    hist_kwargs.setdefault("linewidth", 1.0)

    # Draw the histogram using seaborn's dedicated histogram function.
    sns.histplot(x=series, bins=bins, ax=ax, **hist_kwargs)

    # Recolor each bar by its center's position relative to the median. Bin
    # centers are read back from the drawn bars; scale by the largest distance
    # so the blue/green endpoints are reached at the extremes of the data.
    bars = [p for p in ax.patches if p.get_width() > 0]
    centers = [p.get_x() + p.get_width() / 2 for p in bars]
    max_dist = max((abs(c - median) for c in centers), default=0.0)

    for center, patch in zip(centers, bars):
        if max_dist == 0:
            weight = 0.5  # all bars equidistant from the median -> neutral teal
        else:
            # t in [-1, 1]: -1 far below median, +1 far above.
            t = (center - median) / max_dist
            weight = (t + 1) / 2  # map to [0, 1] for the blue->green blend
        patch.set_facecolor(_blend(weight))

    # Bold, professional title in white.
    ax.set_title(
        title, color="white", fontweight="bold", fontsize=14, fontfamily="sans-serif"
    )

    # White axis labels in the same font family.
    ax.set_xlabel("Value", color="white", fontfamily="sans-serif")
    ax.set_ylabel("Frequency", color="white", fontfamily="sans-serif")

    # White tick labels and axis spines for contrast on black.
    ax.tick_params(colors="white")
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontfamily("sans-serif")
    for spine in ax.spines.values():
        spine.set_color("white")

    return ax
