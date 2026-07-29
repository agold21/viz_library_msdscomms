# viz_library_msdscomms

A small Python visualization library that makes attractive, consistent plots
with one line of code. Every plot shares a single visual language:

- a **blue → green** color encoding keyed to the **median** — marks *below*
  the median trend blue, marks *above* trend green, and the further from the
  median a value sits, the more saturated its color; and
- a professional **dark theme** — black background, white text, a clean
  sans-serif font, bold titles, and white outlines.

Built on [seaborn](https://seaborn.pydata.org/) and
[matplotlib](https://matplotlib.org/).

> **Note on names:** you install the package as `viz-library-msdscomms` but
> import it as `visualizer_alex`.

## Installation

From a local clone (editable/development install):

```bash
pip install -e .
```

This pulls in the dependencies: `pandas`, `matplotlib`, and `seaborn`.

## Quick start

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from visualizer_alex import histogram, heatmap, scatterplot

# 1. Histogram — bars colored by their distance from the median
histogram(np.random.normal(50, 15, 1000), bins=20, title="Distribution")

# 2. Heatmap — a blue→green colormap centered on the median
df = pd.DataFrame(np.random.normal(size=(200, 5)), columns=list("ABCDE"))
heatmap(df.corr(), title="Correlation Heatmap")

# 3. Scatter — points colored by their y-value relative to the median
scatterplot(x=df["A"], y=df["B"], color_by="y", title="A vs. B")

plt.show()
```

Each function returns a matplotlib `Axes`, so you can keep customizing it,
drop it into a subplot grid, or save it. When saving, pass the figure's
face color so the black background is preserved:

```python
ax = histogram(data, title="My Plot")
ax.figure.savefig("plot.png", facecolor=ax.figure.get_facecolor())
```

## Functions

### `histogram(data, bins=10, title="Histogram", ax=None, **hist_kwargs)`

Histogram (via `seaborn.histplot`) whose bars are colored by each bar's
center relative to the median of the data.

- `data` — array-like or `pandas.Series` (NaNs are dropped)
- `bins` — number of bins
- `title` — bold title text
- `ax` — draw onto an existing `Axes` (a new figure is created if omitted)

### `heatmap(data, title="Heatmap", annot=True, fmt=".2f", ax=None, **heatmap_kwargs)`

Heatmap (via `seaborn.heatmap`) using the blue→green blend as a continuous
colormap centered on the median — blue below, teal at, green above. Includes a
colorbar that makes the encoding self-explanatory. Ideal for correlation
matrices.

- `data` — 2D array-like or `pandas.DataFrame` (e.g. `df.corr()`)
- `annot` — write each cell's value on the map
- `fmt` — format string for the annotations

### `scatterplot(x=None, y=None, data=None, color_by="y", title="Scatter Plot", ax=None, colorbar=True, **scatter_kwargs)`

Scatter plot (via `seaborn.scatterplot`) with each point colored by one
coordinate relative to that coordinate's median.

- `x`, `y` — array-likes, or column names when `data` is a `DataFrame`
- `data` — optional `DataFrame` source for `x`/`y` column names
- `color_by` — `"y"` (default) or `"x"`: which coordinate drives the color
- `colorbar` — add a colorbar explaining the blue→green encoding

All three accept extra keyword arguments that are forwarded to the underlying
seaborn function.
