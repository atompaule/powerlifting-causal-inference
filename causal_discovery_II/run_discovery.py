"""
tetrad-only causal discovery

algorithms: pc and fci

ci tests:

- cg: conditional gaussian likelihood ratio test (IndTestConditionalGaussianLrt) -- main test
- gsq: g^2 (IndTestGSquare) -- sensitivity check without gaussian assumption
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import importlib.resources

import jpype
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# tetrad is a java library, so jvm must be started before importing anything from it
home = subprocess.run(
    ["/usr/libexec/java_home", "-v", "17+"], capture_output=True, text=True
).stdout.strip()
os.environ["JAVA_HOME"] = home
jar = str(importlib.resources.files("pytetrad") / "resources" / "tetrad-current.jar")
jpype.startJVM(classpath=[jar])


from pytetrad.tools.TetradSearch import TetradSearch

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data_preprocessing" / "squat_equipment_filtered.csv"
OUT_ROOT = Path(__file__).resolve().parent / "results"

VARIABLES = [
    "Age",
    "BodyweightKg",
    "Sex",
    "Equipment",
    "Best3SquatKg",
    "Year",
    "ParentFederation",
]
CONTINUOUS = ["Age", "BodyweightKg", "Best3SquatKg", "Year"]
DISCRETE = ["Sex", "Equipment", "ParentFederation"]
COLOR = "#5bc0de"

TESTS = ["cg", "gsq"]

ALPHA = 0.05  # standard

# how many bins to use for quantile-binning continuous variables under discrete test (G^2)
N_BINS = 10

# how many categories to discretize continuous parents in CG
# necessary to model continuous->discrete relationships
# py-tetrad default is 3
CG_NUM_CATEGORIES = 3

# background knowledge: year/sex/age are mutually independent and exogenous
EXOGENOUS = ["Year", "Sex", "Age"]


def load_data(test: str) -> pd.DataFrame:
    """encode continuous variables as float64, discrete variables as string

    special case G^2: discretize continuous variables -- quantile-binned and passed as strings
    """
    df = pd.read_csv(DATA_PATH, usecols=VARIABLES)[VARIABLES].copy()
    for col in DISCRETE:
        df[col] = df[col].astype(str)
    if test == "gsq":
        for col in CONTINUOUS:
            df[col] = pd.qcut(df[col], q=N_BINS, labels=False, duplicates="drop")
            df[col] = df[col].astype(str)
    return df[VARIABLES]


_MARK = {"TAIL": "-", "ARROW": ">", "CIRCLE": "o"}
_LEFT = {"TAIL": "-", "ARROW": "<", "CIRCLE": "o"}


def extract_edges(java_graph):
    edges = []
    for edge in java_graph.getEdges():
        n1 = str(edge.getNode1().getName())
        n2 = str(edge.getNode2().getName())
        e1 = edge.getEndpoint1().name()
        e2 = edge.getEndpoint2().name()
        label = f"{n1} {_LEFT[e1]}-{_MARK[e2]} {n2}"
        edges.append((n1, n2, e1, e2, label))
    return edges


def adjacency_frame(edges, names: list[str]) -> pd.DataFrame:
    idx = {n: k for k, n in enumerate(names)}
    mat = np.full((len(names), len(names)), ".", dtype=object)
    for n1, n2, e1, e2, _ in edges:
        mat[idx[n1], idx[n2]] = _MARK[e2]
        mat[idx[n2], idx[n1]] = _MARK[e1]
    return pd.DataFrame(mat, index=names, columns=names)


def draw_graph(edges, names: list[str], title: str, path: Path) -> None:
    angles = np.linspace(0, 2 * np.pi, len(names), endpoint=False)
    pos = {n: np.array([np.cos(t), np.sin(t)]) for n, t in zip(names, angles)}

    fig, ax = plt.subplots(figsize=(8, 8))
    for n, (x, y) in pos.items():
        ax.scatter([x], [y], s=2600, c=COLOR, zorder=2, edgecolors="black")
        ax.text(
            x, y, n, ha="center", va="center", fontsize=8, fontweight="bold", zorder=3
        )

    def shorten(p, q, frac=0.16):
        p, q = np.array(p), np.array(q)
        return p + (q - p) * frac, q - (q - p) * frac

    for n1, n2, e1, e2, _ in edges:
        a, b = shorten(pos[n1], pos[n2])
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#444", lw=1.4, zorder=1)
        for endpoint, tip, other in ((e1, a, b), (e2, b, a)):
            if endpoint == "ARROW":
                ax.annotate(
                    "",
                    xy=tip,
                    xytext=(tip + other) / 2,
                    arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.4),
                    zorder=1,
                )
            elif endpoint == "CIRCLE":
                ax.scatter(
                    [tip[0]],
                    [tip[1]],
                    s=70,
                    facecolors="white",
                    edgecolors="#444",
                    zorder=2,
                )

    ax.set_title(title, fontsize=12)
    ax.axis("off")
    ax.margins(0.18)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def run_test(test: str) -> None:
    out_dir = OUT_ROOT / test / str(ALPHA)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(test)
    print(f"\n--- {test} --- {len(df):,} rows")

    def search_with(algorithm_name: str):
        search = TetradSearch(df)
        if test == "cg":
            search.use_conditional_gaussian_test(
                alpha=ALPHA,
                discretize=True,
                num_categories_to_discretize=CG_NUM_CATEGORIES,
            )
        elif test == "gsq":
            search.use_g_square(alpha=ALPHA)
        else:
            raise ValueError(f"unknown test: {test}")

        # apply background knowledge
        # tier 0: exogenous + mutually independent; tier 1: everything else.
        # forbidding edges within tier 0 gives mutual independence; the tier order
        # forbids edges from tier 1 back into tier 0 (exogeneity).
        for var in EXOGENOUS:
            search.add_to_tier(0, var) # vars >0 cannot cause vars 0
        for var in VARIABLES:
            if var not in EXOGENOUS:
                search.add_to_tier(1, var)
        search.set_tier_forbidden_within(0, True) # vars 0 cannot cause other vars 0

        algorithm = getattr(search, algorithm_name)
        algorithm()
        print(search.get_string())
        return search.get_java()

    print("PC...")
    pc_graph = search_with("run_pc")
    pc_edges = extract_edges(pc_graph)
    adjacency_frame(pc_edges, VARIABLES).to_csv(out_dir / "pc_adjacency.csv")
    (out_dir / "pc_edges.txt").write_text("\n".join(l for *_, l in pc_edges) + "\n")
    draw_graph(pc_edges, VARIABLES, f"PC -- {test}", out_dir / "pc_graph.png")

    print("FCI...")
    fci_graph = search_with("run_fci")
    fci_edges = extract_edges(fci_graph)
    adjacency_frame(fci_edges, VARIABLES).to_csv(out_dir / "fci_adjacency.csv")
    (out_dir / "fci_edges.txt").write_text("\n".join(l for *_, l in fci_edges) + "\n")
    draw_graph(fci_edges, VARIABLES, f"FCI (PAG) -- {test}", out_dir / "fci_graph.png")

    print(f"PC: {len(pc_edges)} edges, FCI: {len(fci_edges)} edges")


def main() -> None:
    tests = sys.argv[1:] or TESTS
    for test in tests:
        run_test(test)
    print("\nDone.")


if __name__ == "__main__":
    main()
