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

## Examples

A complete, runnable example on the Palmer Penguins dataset lives in
[`examples/penguins_gallery.py`](examples/penguins_gallery.py):

```bash
python examples/penguins_gallery.py
```

It loads real ecological data and displays all three plots.

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

## Development

Install the package along with the development tools (`build`, `twine`,
`pytest`):

```bash
pip install -e ".[dev]"
```

## Publishing to PyPI

The project builds a standard wheel and source distribution. To publish a new
release:

1. **Bump the version** in `pyproject.toml` (`[project].version`). PyPI rejects
   re-uploads of an existing version, so every release needs a new number.

2. **Build fresh artifacts** (clear out any stale ones first):

   ```bash
   rm -rf dist/
   python -m build
   ```

   This creates `dist/*.whl` and `dist/*.tar.gz`.

3. **Validate the artifacts** with PyPI's checker:

   ```bash
   twine check dist/*
   ```

4. **(Recommended) Dry run on TestPyPI** before the real thing:

   ```bash
   twine upload --repository testpypi dist/*
   ```

   Then confirm it installs (pulling dependencies from real PyPI):

   ```bash
   pip install --index-url https://test.pypi.org/simple/ \
       --extra-index-url https://pypi.org/simple/ viz-library-msdscomms
   ```

5. **Upload to PyPI**:

   ```bash
   twine upload dist/*
   ```

Authentication uses an API token: when prompted, enter `__token__` as the
username and your PyPI token (starting with `pypi-`) as the password. You can
store it in `~/.pypirc` to avoid re-entering it.
