"""
causal effect estimation for equipment -> squat performance.

we estimate the effect of each equipment category (vs raw) on best3, via backdoor adjustment.

reasoning: temporal ordering from background knowledge as foundation for choosing Z.
everything in Z precedes equipment choice; Z is a set of confounders (no mediators, no colliders).
-> Z = {Sex, Age, BodyweightKg, Year, ParentFederation}.

two models are compared:
-> baseline: Best3SquatKg <- Equipment (raw association)
-> adjusted: Best3SquatKg <- Equipment, Z (backdoor-adjusted effect)

continuous confounders included linearly and quadratically, to account for nonlinear relationships with performance.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data_preprocessing" / "squat_equipment_filtered.csv"
OUT_DIR = Path(__file__).resolve().parent / "results"

OUTCOME = "Best3SquatKg"
TREATMENT = "Equipment"
TREATMENT_REF = "Raw"

# backdoor adjustment set (all pre-treatment, per the discovery tiers)
DISCRETE_Z = ["Sex", "ParentFederation"]
FED_REF = "IPF"
# entered as linear + quadratic (centered)
CONTINUOUS_Z = [
    "BodyweightKg",
    "Age",
    "Year",
]

# robust (heteroskedasticity-consistent) standard errors
COV_TYPE = "HC1"
COLOR = "#5bc0de"
COLOR_NAIVE = "#bbbbbb"


def load_data() -> pd.DataFrame:
    cols = [OUTCOME, TREATMENT] + DISCRETE_Z + CONTINUOUS_Z
    df = pd.read_csv(DATA_PATH, usecols=cols)[cols].copy()
    # center continuous variables so the quadratic terms are not collinear with linear ones
    for col in CONTINUOUS_Z:
        df[col + "_c"] = df[col] - df[col].mean()
    return df


def build_formulas() -> tuple[str, str]:
    treat = f"C({TREATMENT}, Treatment(reference='{TREATMENT_REF}'))"
    baseline = f"{OUTCOME} ~ {treat}"

    terms = [treat, "C(Sex)", f"C(ParentFederation, Treatment(reference='{FED_REF}'))"]
    for col in CONTINUOUS_Z:
        terms.append(f"{col}_c")
        terms.append(f"I({col}_c ** 2)")
    adjusted = f"{OUTCOME} ~ " + " + ".join(terms)
    return baseline, adjusted


def treatment_effects(fit) -> pd.DataFrame:
    ci = fit.conf_int()
    rows = []
    for name in fit.params.index:
        if TREATMENT not in name:
            continue
        # param name looks like: C(Equipment, Treatment(...))[T.Single-ply]
        category = name.split("[T.")[-1].rstrip("]")
        rows.append(
            {
                "category": category,
                "effect_kg": fit.params[name],
                "ci_low": ci.loc[name, 0],
                "ci_high": ci.loc[name, 1],
                "p": fit.pvalues[name],
            }
        )
    return pd.DataFrame(rows).set_index("category")


def plot_effects(baseline: pd.DataFrame, adjusted: pd.DataFrame, path: Path) -> None:
    cats = list(adjusted.index)
    x = np.arange(len(cats))
    w = 0.38

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for offset, tbl, color, label in (
        (-w / 2, baseline, COLOR_NAIVE, "baseline (unadjusted)"),
        (w / 2, adjusted, COLOR, "adjusted (backdoor)"),
    ):
        t = tbl.reindex(cats)
        err = np.vstack([t.effect_kg - t.ci_low, t.ci_high - t.effect_kg])
        ax.bar(
            x + offset,
            t.effect_kg,
            width=w,
            color=color,
            edgecolor="black",
            label=label,
            yerr=err,
            capsize=4,
        )

    ax.axhline(0, color="#444", lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    ax.set_ylabel(f"effect on {OUTCOME} vs {TREATMENT_REF} (kg)")
    ax.set_title("Equipment effect on squat: baseline vs backdoor-adjusted")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    print(f"loaded {len(df):,} rows")

    baseline_formula, adjusted_formula = build_formulas()
    print(f"\baseline:    {baseline_formula}")
    print(f"adjusted: {adjusted_formula}")

    baseline_fit = smf.ols(baseline_formula, data=df).fit(cov_type=COV_TYPE)
    adjusted_fit = smf.ols(adjusted_formula, data=df).fit(cov_type=COV_TYPE)

    baseline_eff = treatment_effects(baseline_fit)
    adjusted_eff = treatment_effects(adjusted_fit)

    table = baseline_eff.join(adjusted_eff, lsuffix="_baseline", rsuffix="_adj")
    print("\n=== Equipment effect on Best3SquatKg (kg vs Raw) ===")
    print(table.round(2).to_string())

    (OUT_DIR / "adjusted_model_summary.txt").write_text(str(adjusted_fit.summary()))
    table.to_csv(OUT_DIR / "equipment_effects.csv")
    plot_effects(baseline_eff, adjusted_eff, OUT_DIR / "equipment_effects.png")
    print(f"\nwrote results to {OUT_DIR}")


if __name__ == "__main__":
    main()
