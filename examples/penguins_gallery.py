"""Example: using visualizer_alex on the Palmer Penguins dataset.

This script demonstrates all three plotting functions from the library on a
real ecological dataset (344 Antarctic penguins with body measurements). Each
function draws on the shared blue->green median encoding and dark theme.

Run it with:

    python examples/penguins_gallery.py

The Palmer Penguins data ships with seaborn (downloaded and cached on first
use, so an internet connection is needed the first time).
"""

import matplotlib.pyplot as plt
import seaborn as sns

from visualizer_alex import heatmap, histogram, scatterplot

# The measurement columns we'll visualize.
MEASUREMENTS = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]


def main() -> None:
    # Load the dataset and drop rows with missing measurements.
    penguins = sns.load_dataset("penguins").dropna()
    print(f"Loaded {len(penguins)} penguins.")
    print(f"Median body mass: {penguins['body_mass_g'].median():.0f} g")

    # 1. Histogram — distribution of body mass. Bars below the median are blue,
    #    bars above are green.
    ax_hist = histogram(penguins["body_mass_g"], bins=20, title="Penguin Body Mass")
    ax_hist.set_xlabel("Body mass (g)")

    # 2. Heatmap — correlations among the four measurements, using the
    #    blue->green blend as a continuous colormap centered on the median.
    ax_heat = heatmap(penguins[MEASUREMENTS].corr(), title="Measurement Correlations")

    # 3. Scatter — flipper length vs. body mass, with each point colored by its
    #    body mass relative to the median.
    ax_scatter = scatterplot(
        x=penguins["flipper_length_mm"],
        y=penguins["body_mass_g"],
        color_by="y",
        title="Flipper Length vs. Body Mass",
    )
    ax_scatter.set_xlabel("Flipper length (mm)")
    ax_scatter.set_ylabel("Body mass (g)")

    # Display all three figures.
    plt.show()


if __name__ == "__main__":
    main()
