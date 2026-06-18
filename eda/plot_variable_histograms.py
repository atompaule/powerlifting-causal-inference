from math import ceil
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

HERE = Path(__file__).resolve().parent
CSV = HERE / "../data_preprocessing/squat_equipment_filtered.csv"
OUT = HERE / "variable_histograms.png"

NUMERIC = ["Age", "BodyweightKg", "Best3SquatKg", "Year"]
CATEGORICAL = ["Sex", "Equipment", "ParentFederation"]

EQUIP_ORDER = ["Raw", "Wraps", "Single-ply", "Multi-ply", "Unlimited"]

plt.rcParams.update(
    {
        "figure.facecolor": "#1c1c1e",
        "axes.facecolor": "#2c2c2e",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "text.color": "white",
        "axes.titlecolor": "white",
        "grid.color": "#3c3c3e",
        "axes.edgecolor": "#3c3c3e",
    }
)
ACCENT = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#A29BFE", "#74B9FF", "#55EFC4"]


def thousands(ax, axis="y"):
    fmt = mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def plot_numeric(ax, s: pd.Series, color: str):
    s = s.dropna()
    ax.hist(s, bins=60, color=color, alpha=0.85, edgecolor="none")
    med = s.median()
    ax.axvline(
        med, color="white", linestyle="--", linewidth=1.4, label=f"median {med:g}"
    )
    ax.set_title(s.name, fontsize=13, fontweight="bold")
    ax.set_xlabel(s.name)
    ax.set_ylabel("# entries")
    thousands(ax, "y")
    ax.legend(fontsize=9)


def plot_categorical(ax, s: pd.Series, color: str):
    counts = s.value_counts()
    if s.name == "Equipment":
        counts = counts.reindex([c for c in EQUIP_ORDER if c in counts.index])

    horizontal = counts.size > 6 or s.name == "ParentFederation"
    total = counts.sum()
    if horizontal:
        counts = counts.sort_values()
        ax.barh(counts.index, counts.values, color=color, edgecolor="none")
        thousands(ax, "x")
        for y, v in enumerate(counts.values):
            ax.text(
                v,
                y,
                f" {v:,} ({100 * v / total:.0f}%)",
                va="center",
                ha="left",
                fontsize=7.5,
                color="white",
            )
        ax.margins(x=0.18)
    else:
        ax.bar(counts.index, counts.values, color=color, edgecolor="none")
        thousands(ax, "y")
        for x, v in enumerate(counts.values):
            ax.text(
                x,
                v,
                f"{v:,}\n{100 * v / total:.0f}%",
                ha="center",
                va="bottom",
                fontsize=8,
                color="white",
            )
        ax.margins(y=0.15)
        plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
    ax.set_title(s.name, fontsize=13, fontweight="bold")
    ax.set_xlabel("# entries" if horizontal else "")


def main():
    df = pd.read_csv(CSV)
    print(f"Loaded {CSV.name}: {len(df):,} rows")

    panels = NUMERIC + CATEGORICAL
    ncols = 3
    nrows = ceil(len(panels) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(20, 5.2 * nrows))
    fig.suptitle(
        "Variable Distributions\n"
        f"{len(df):,} entries (one per contestant, SBD, Tested, Sanctioned)",
        fontsize=18,
        fontweight="bold",
        y=0.995,
    )
    axes = axes.ravel()

    for i, col in enumerate(panels):
        color = ACCENT[i % len(ACCENT)]
        if col in NUMERIC:
            plot_numeric(axes[i], df[col], color)
        else:
            plot_categorical(axes[i], df[col], color)

    for ax in axes[len(panels) :]:
        ax.set_visible(False)

    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Done: {OUT.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
