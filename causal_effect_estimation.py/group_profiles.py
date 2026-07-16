"""per-equipment-category profiles of all variables used in discovery/estimation.

continuous variables (Best3SquatKg, BodyweightKg, Age, Year) -> group mean.
discrete variables (Sex, ParentFederation) -> share per level in percent.

output is one wide table (row per equipment category), ready for plotting.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data_preprocessing" / "squat_equipment_filtered.csv"
OUT_DIR = Path(__file__).resolve().parent / "results"

CONTINUOUS = ["Best3SquatKg", "BodyweightKg", "Age", "Year"]
DISCRETE = ["Sex", "ParentFederation"]
COLOR = "#5bc0de"

# rows of the plot: (column in the profile table, axis label)
PLOT_ROWS = [
    ("Best3SquatKg", "mean Best3SquatKg (kg)"),
    ("BodyweightKg", "mean BodyweightKg (kg)"),
    ("Age", "mean Age (years)"),
    ("Year", "mean Year"),
    ("pct_Sex_M", "share male (%)"),
    ("pct_ParentFederation_IPF", "share IPF (%)"),
]

# plot shows each category's difference vs the reference category
PLOT_REF = "Raw"
PLOT_EXCLUDE = ["Unlimited"]


def main() -> None:
    df = pd.read_csv(DATA_PATH, usecols=["Equipment"] + CONTINUOUS + DISCRETE)

    profile = df.groupby("Equipment").agg(
        n=("Equipment", "size"),
        **{col: (col, "mean") for col in CONTINUOUS},
    )

    for col in DISCRETE:
        shares = pd.crosstab(df["Equipment"], df[col], normalize="index") * 100
        shares.columns = [f"pct_{col}_{level}" for level in shares.columns]
        profile = profile.join(shares)

    profile = profile.sort_values("n", ascending=False).round(2)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    profile.to_csv(OUT_DIR / "group_profiles.csv")
    print(profile.to_string())

    plot_profiles(profile, OUT_DIR / "group_profiles.png")
    print(f"\nwrote results to {OUT_DIR}")


def plot_profiles(profile: pd.DataFrame, path: Path) -> None:
    """one row per variable, one horizontal bar per equipment category,
    each bar the difference of the group mean vs the reference category."""
    # top-to-bottom plot order; barh draws bottom-up, hence reversed
    cats = ["Wraps", "Single-ply", "Multi-ply"][::-1]

    fig, axes = plt.subplots(
        len(PLOT_ROWS), 1, figsize=(9, 1.4 * len(PLOT_ROWS)), sharey=True
    )
    for ax, (col, label) in zip(axes, PLOT_ROWS):
        diffs = profile.loc[cats, col] - profile.loc[PLOT_REF, col]
        ax.barh(cats, diffs, color=COLOR, edgecolor="black")
        for i, v in enumerate(diffs):
            ax.text(
                v,
                i,
                f" {v:+.1f} " if abs(v) > 0.05 else " ±0.0 ",
                va="center",
                ha="left" if v >= 0 else "right",
                fontsize=8,
            )
        ax.axvline(0, color="#444", lw=1)
        ax.set_xlabel(f"{label}, difference vs {PLOT_REF}", fontsize=9)
        ax.margins(x=0.15)
        ax.tick_params(labelsize=9)

    fig.suptitle(f"Lifter profiles per equipment category (vs {PLOT_REF})", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    fig.savefig(path, dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
