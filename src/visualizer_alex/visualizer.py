"""Core plotting functions for the visualizer library.

Each function draws with seaborn and shares one visual language: a blue->green
encoding keyed to the median (blue below, green above) on a professional dark
theme. The shared color and styling logic lives in :mod:`visualizer_alex._style`.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ._style import (
    add_bluegreen_colorbar,
    apply_dark_style,
    blend,
    bluegreen_cmap,
    median_weights,
    style_colorbar_white,
    use_preferred_fonts,
)


def histogram(data, bins: int = 10, title: str = "Histogram", ax=None, **hist_kwargs):
    """Plot a histogram colored by each bar's position relative to the median.

    Drawn with :func:`seaborn.histplot`. Bars below the median are shaded toward
    blue and bars above toward green, more saturated the further from the median.
    Styled with a black background, white text, a bold title, and white outlines.

    Parameters
    ----------
    data : array-like or pandas.Series
        The values to histogram. Missing values (NaN) are dropped.
    bins : int, default 10
        Number of histogram bins passed to ``seaborn.histplot``.
    title : str, default "Histogram"
        Bold title rendered at the top of the plot.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. If omitted, a new figure and axes are created.
    **hist_kwargs
        Additional keyword arguments forwarded to ``seaborn.histplot``.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the styled, colored histogram.
    """
    series = pd.Series(data).dropna()
    if series.empty:
        raise ValueError("`data` contains no non-null values to plot.")

    median = series.median()
    use_preferred_fonts()

    if ax is None:
        _, ax = plt.subplots()

    hist_kwargs.setdefault("edgecolor", "white")
    hist_kwargs.setdefault("linewidth", 1.0)
    sns.histplot(x=series, bins=bins, ax=ax, **hist_kwargs)

    # Recolor each bar by its center's position relative to the median.
    bars = [p for p in ax.patches if p.get_width() > 0]
    centers = [p.get_x() + p.get_width() / 2 for p in bars]
    for patch, weight in zip(bars, median_weights(centers, median)):
        patch.set_facecolor(blend(weight))

    apply_dark_style(ax, title, xlabel="Value", ylabel="Frequency")
    return ax


def heatmap(data, title: str = "Heatmap", annot: bool = True, fmt: str = ".2f",
            ax=None, **heatmap_kwargs):
    """Plot a heatmap using a blue->green colormap centered on the median.

    Drawn with :func:`seaborn.heatmap`. Cells below the median are blue and
    cells above are green, transitioning through teal at the median (via
    seaborn's ``center``). Ideal for correlation matrices or any 2D grid.
    Styled with a black background, white text, a bold title, and white
    gridlines, plus a colorbar that makes the encoding self-explanatory.

    Parameters
    ----------
    data : 2D array-like or pandas.DataFrame
        The matrix of values to plot (e.g. ``df.corr()``).
    title : str, default "Heatmap"
        Bold title rendered at the top of the plot.
    annot : bool, default True
        Whether to write each cell's value on the heatmap.
    fmt : str, default ".2f"
        Format string for the cell annotations.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. If omitted, a new figure and axes are created.
    **heatmap_kwargs
        Additional keyword arguments forwarded to ``seaborn.heatmap``.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the styled heatmap.
    """
    df = pd.DataFrame(data)
    flat = pd.Series(df.to_numpy().ravel()).dropna()
    if flat.empty:
        raise ValueError("`data` contains no non-null values to plot.")

    median = flat.median()
    use_preferred_fonts()

    if ax is None:
        _, ax = plt.subplots()

    # White gridlines separate the cells against the dark theme.
    heatmap_kwargs.setdefault("linewidths", 0.5)
    heatmap_kwargs.setdefault("linecolor", "white")
    annot_kws = heatmap_kwargs.pop("annot_kws", {"color": "white"})

    # `center=median` makes the diverging colormap put teal at the median,
    # blue below and green above.
    sns.heatmap(
        df, cmap=bluegreen_cmap(), center=median, annot=annot, fmt=fmt,
        ax=ax, annot_kws=annot_kws, **heatmap_kwargs,
    )

    apply_dark_style(ax, title)

    cbar = ax.collections[-1].colorbar
    if cbar is not None:
        style_colorbar_white(cbar)
    return ax


def scatterplot(x=None, y=None, data=None, color_by: str = "y",
                title: str = "Scatter Plot", ax=None, colorbar: bool = True,
                **scatter_kwargs):
    """Plot a scatter with points colored by their position relative to a median.

    Drawn with :func:`seaborn.scatterplot`. Each point is colored by one
    variable (``color_by``) relative to that variable's median: points below
    the median are blue and points above are green, more saturated the further
    away. Styled with a black background, white text, a bold title, and white
    point outlines, plus a colorbar explaining the encoding.

    Parameters
    ----------
    x, y : array-like, or str when ``data`` is given
        The point coordinates. If ``data`` is a DataFrame, ``x`` and ``y`` may
        be column names instead.
    data : pandas.DataFrame, optional
        Source frame when ``x`` and ``y`` are column names.
    color_by : {"y", "x"}, default "y"
        Which coordinate determines each point's color relative to its median.
    title : str, default "Scatter Plot"
        Bold title rendered at the top of the plot.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. If omitted, a new figure and axes are created.
    colorbar : bool, default True
        Whether to add a colorbar explaining the blue->green encoding.
    **scatter_kwargs
        Additional keyword arguments forwarded to ``seaborn.scatterplot``.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the styled scatter plot.
    """
    if color_by not in ("x", "y"):
        raise ValueError("`color_by` must be 'x' or 'y'.")

    # Resolve inputs into a two-column frame, whether passed as arrays or as
    # column names against a DataFrame.
    if data is not None and isinstance(x, str) and isinstance(y, str):
        source = pd.DataFrame(data)
        frame = pd.DataFrame({"x": source[x], "y": source[y]})
        xlabel, ylabel = x, y
    else:
        frame = pd.DataFrame({"x": pd.Series(x), "y": pd.Series(y)})
        xlabel, ylabel = "x", "y"

    frame = frame.dropna()
    if frame.empty:
        raise ValueError("No non-null (x, y) pairs to plot.")

    color_values = frame[color_by]
    median = color_values.median()
    use_preferred_fonts()

    if ax is None:
        _, ax = plt.subplots()

    scatter_kwargs.setdefault("edgecolor", "white")
    scatter_kwargs.setdefault("linewidth", 0.6)
    scatter_kwargs.setdefault("s", 60)
    sns.scatterplot(x=frame["x"], y=frame["y"], ax=ax, **scatter_kwargs)

    # Recolor the drawn points by their color_by value vs. the median.
    weights = median_weights(color_values.tolist(), median)
    ax.collections[-1].set_facecolors([blend(w) for w in weights])

    apply_dark_style(ax, title, xlabel=xlabel, ylabel=ylabel)

    if colorbar:
        label = f"{ylabel if color_by == 'y' else xlabel} (relative to median)"
        add_bluegreen_colorbar(ax, color_values.tolist(), median, label=label)
    return ax
