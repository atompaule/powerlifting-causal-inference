from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

HERE = Path(__file__).resolve().parent
CSV = HERE / "../data_preprocessing/squat_equipment_filtered.csv"
OUT = HERE / "correlation_clouds.png"

CONTINUOUS = ["Age", "BodyweightKg", "Best3SquatKg", "Year"]
CATEGORICAL = ["Sex", "Equipment", "ParentFederation"]
VARS = CONTINUOUS + CATEGORICAL

SAMPLE = 50_000  # number of samples randomly drawn per scatter panel
SEED = 42
TOPK = 6  # max categories drawn per categorical variable
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
CLOUD = "#4ECDC4"  # scatter clouds
BOX = "#74B9FF"  # box plots
BAR = "#A29BFE"  # diagonal count bars
REG = "#FFE66D"  # regression line
HEATMAP = "magma"


def correlation_ratio(cats: pd.Series, values: pd.Series) -> float:
    """η: fraction of the continuous variable's variance explained by the
    categorical grouping (0 = none, 1 = group means fully separate)."""
    d = pd.DataFrame({"c": cats.values, "v": values.values}).dropna()
    grand = d["v"].mean()
    ss_tot = ((d["v"] - grand) ** 2).sum()
    if ss_tot == 0:
        return np.nan
    ss_between = (
        d.groupby("c")["v"].apply(lambda g: len(g) * (g.mean() - grand) ** 2).sum()
    )
    return float(np.sqrt(ss_between / ss_tot))


def cramers_v(a: pd.Series, b: pd.Series) -> float:
    """Cramér's V: association between two categoricals (0 = independent, 1 = one
    determines the other), computed on all levels."""
    ct = pd.crosstab(a, b)
    if ct.shape[0] < 2 or ct.shape[1] < 2:
        return np.nan
    chi2 = chi2_contingency(ct, correction=False)[0]
    n = ct.values.sum()
    denom = min(ct.shape) - 1
    return float(np.sqrt((chi2 / n) / denom)) if denom > 0 else np.nan


def levels_of(col: str, s: pd.Series) -> list:
    if col == "Equipment":
        return [c for c in EQUIP_ORDER if c in s.unique()]
    if col == "Sex":
        return [v for v in ["M", "F"] if v in s.unique()]
    return list(s.value_counts().index[:TOPK])  # top-K by frequency


def annotate(ax, text: str):
    ax.text(
        0.04,
        0.96,
        text,
        transform=ax.transAxes,
        fontsize=8.5,
        va="top",
        ha="left",
        color="white",
        fontweight="bold",
        bbox=dict(facecolor="#1c1c1e", alpha=0.65, edgecolor="none", pad=2),
    )


def regline(ax, x, y):
    """Least-squares line of y on x, drawn across the observed x-range."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 2:
        return
    slope, intercept = np.polyfit(x[m], y[m], 1)
    xs = np.array([x[m].min(), x[m].max()])
    ax.plot(xs, slope * xs + intercept, color=REG, lw=1.6, ls="--", alpha=0.95)


def draw_boxes(ax, df, cat_col, cont_col, horizontal):
    """Box plot of the continuous variable per category. Returns (positions,
    continuous) arrays aligned row-wise, for the regression line."""
    levels = levels_of(cat_col, df[cat_col])
    pos_of = {lv: i + 1 for i, lv in enumerate(levels)}
    sub = df[df[cat_col].isin(levels)]
    groups = [sub.loc[sub[cat_col] == lv, cont_col].dropna().values for lv in levels]

    orient = "horizontal" if horizontal else "vertical"
    bp = ax.boxplot(
        groups, orientation=orient, showfliers=False, patch_artist=True, widths=0.6
    )
    for patch in bp["boxes"]:
        patch.set(facecolor=BOX, alpha=0.75, edgecolor="white", linewidth=0.6)
    for med in bp["medians"]:
        med.set(color="white", linewidth=1.2)
    for line in bp["whiskers"] + bp["caps"]:
        line.set(color="#999", linewidth=0.6)

    pos = range(1, len(levels) + 1)
    if horizontal:
        ax.set_yticks(pos)
        ax.set_yticklabels(levels, fontsize=6)
        ax.tick_params(axis="x", labelsize=6)
    else:
        ax.set_xticks(pos)
        ax.set_xticklabels(levels, fontsize=6, rotation=30, ha="right")
        ax.tick_params(axis="y", labelsize=6)

    return sub[cat_col].map(pos_of).values, sub[cont_col].values


def draw_heatmap(ax, df, row_col, col_col):
    rl, cl = levels_of(row_col, df[row_col]), levels_of(col_col, df[col_col])
    # P(column category | row category)
    ct = pd.crosstab(df[row_col], df[col_col], normalize="index").reindex(
        index=rl, columns=cl
    )
    ax.imshow(ct.values, cmap=HEATMAP, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(cl)))
    ax.set_xticklabels(cl, fontsize=6, rotation=30, ha="right")
    ax.set_yticks(range(len(rl)))
    ax.set_yticklabels(rl, fontsize=6)
    for yi in range(len(rl)):
        for xi in range(len(cl)):
            v = ct.values[yi, xi]
            ax.text(
                xi,
                yi,
                f"{v * 100:.0f}",
                ha="center",
                va="center",
                fontsize=6,
                color="white" if v < 0.55 else "black",
            )


def main():
    df = pd.read_csv(CSV)
    print(f"Loaded {Path(CSV).name}: {len(df):,} rows")
    sample = df.sample(min(SAMPLE, len(df)), random_state=SEED)

    n = len(VARS)
    fig, axes = plt.subplots(n, n, figsize=(3.3 * n, 3.3 * n))
    fig.suptitle(
        "Correlation Clouds\n" f"{SAMPLE}/{len(df):,} rows",
        fontsize=15,
        fontweight="bold",
        y=0.997,
    )

    for i, R in enumerate(VARS):  # R = row variable → y-axis
        for j, C in enumerate(VARS):  # C = column variable → x-axis
            ax = axes[i, j]
            Rc, Cc = R in CONTINUOUS, C in CONTINUOUS

            if i == j:  # diagonal
                if Rc:
                    ax.hist(
                        df[R].dropna(),
                        bins=55,
                        color=CLOUD,
                        alpha=0.85,
                        edgecolor="none",
                    )
                else:
                    lv = levels_of(R, df[R])
                    cnt = df[R].value_counts().reindex(lv)
                    ax.barh(range(len(lv)), cnt.values, color=BAR, edgecolor="none")
                    ax.set_yticks(range(len(lv)))
                    ax.set_yticklabels(lv, fontsize=6)
                ax.tick_params(labelsize=6)

            elif Rc and Cc:  # continuous × continuous
                ax.scatter(
                    sample[C],
                    sample[R],
                    s=5,
                    alpha=0.15,
                    color=CLOUD,
                    edgecolors="none",
                    rasterized=True,
                )
                regline(ax, df[C], df[R])
                annotate(
                    ax,
                    f"r = {df[C].corr(df[R], 'pearson'):+.2f}\n"
                    f"ρ = {df[C].corr(df[R], 'spearman'):+.2f}",
                )
                ax.tick_params(labelsize=6)

            elif Rc and not Cc:  # x categorical, y continuous
                draw_boxes(ax, df, cat_col=C, cont_col=R, horizontal=False)
                annotate(ax, f"η = {correlation_ratio(df[C], df[R]):.2f}")

            elif Cc and not Rc:  # x continuous, y categorical
                draw_boxes(ax, df, cat_col=R, cont_col=C, horizontal=True)
                annotate(ax, f"η = {correlation_ratio(df[R], df[C]):.2f}")

            else:  # categorical × categorical
                draw_heatmap(ax, df, row_col=R, col_col=C)
                annotate(ax, f"V = {cramers_v(df[R], df[C]):.2f}")

            if i == n - 1:
                ax.set_xlabel(C, fontsize=11, fontweight="bold")
            if j == 0:
                ax.set_ylabel(R, fontsize=11, fontweight="bold")

    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Done: {OUT.resolve().relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
