"""
causal discovery runs: PC and FCI, including initial background knowledge.

three runs, each with its own CI test:
- fisherz (naive toy-model baseline -- we have mixed data, so there are more suitable alternatives)
    - only works with linear dependencies
    - only works with gaussian continuous distributions
- gsq (G^2 (with continuous variables quantile-binned))
    - works with any dependencies
    - only works with discrete distributions -- but will work with continous vars if binned, so there'll be some information loss -- works with counts and compares frequencies -- stratisfies z, then compares counts of x-y
    - cell-sparsity problem: (TO DO)
- rcit (randomized conditional independence test (considering non-linear dependences))
    - works with any dependencies -- kernel-based, so detects dependences of arbitrary form
    - works with any distributions
"""

from __future__ import annotations

import itertools
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from causallearn.graph.Endpoint import Endpoint
from causallearn.search.ConstraintBased.FCI import fci
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.PCUtils.BackgroundKnowledge import BackgroundKnowledge
from cg_citest import register_cg

register_cg()  # makes the cg test available in causal-learn


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

TESTS = ["fisherz", "gsq", "rcit"]

ALPHA = 0.05  # standard
N_BINS = 10  # quantile bins for continuous vars under discrete test (e.g., G^2)

# adding background knowledge: year/sex/age are independent and exogenous
INDEPENDENT = ["Year", "Sex", "Age"]
EXOGENOUS = ["Year", "Sex", "Age"]


def encode_for_test(df: pd.DataFrame, test: str) -> np.ndarray:
    """
    discrete variables must be integer-encoded for causal-learn.
    additionally, for the G^2 test, continuous variables must be quantile-binned.
    """
    df = df.copy()
    for col in DISCRETE:
        cats = sorted(df[col].astype(str).unique())
        df[col] = df[col].astype(str).map({c: i for i, c in enumerate(cats)})

    discrete = test == "gsq"
    if discrete:
        for col in CONTINUOUS:
            df[col] = pd.qcut(df[col], q=N_BINS, labels=False, duplicates="drop")

    return df[VARIABLES].to_numpy(dtype=np.int64 if discrete else np.float64)


def build_background_knowledge() -> BackgroundKnowledge:
    bk = BackgroundKnowledge()

    def rx(name: str) -> str:
        return f"^{name}$"

    for a, b in itertools.permutations(INDEPENDENT, 2):
        bk.add_forbidden_by_pattern(rx(a), rx(b))

    for target in EXOGENOUS:
        bk.add_forbidden_by_pattern(".*", rx(target))

    return bk


_MARK = {
    Endpoint.TAIL.value: "-",
    Endpoint.ARROW.value: ">",
    Endpoint.CIRCLE.value: "o",
}


def _mark(endpoint) -> str:
    return _MARK[endpoint.value]


def _edge_string(n1: str, e1, e2, n2: str) -> str:
    left = (
        "o"
        if e1.value == Endpoint.CIRCLE.value
        else ("<" if e1.value == Endpoint.ARROW.value else "-")
    )
    return f"{n1} {left}-{_mark(e2)} {n2}"


def extract_edges(graph):
    edges = []
    for edge in graph.get_graph_edges():
        n1 = edge.get_node1().get_name()
        n2 = edge.get_node2().get_name()
        e1, e2 = edge.get_endpoint1(), edge.get_endpoint2()
        edges.append((n1, n2, e1, e2, _edge_string(n1, e1, e2, n2)))
    return edges


def adjacency_frame(graph, names: list[str]) -> pd.DataFrame:
    idx = {n: k for k, n in enumerate(names)}
    mat = np.full((len(names), len(names)), ".", dtype=object)
    for n1, n2, e1, e2, _ in extract_edges(graph):
        mat[idx[n1], idx[n2]] = _mark(e2)
        mat[idx[n2], idx[n1]] = _mark(e1)
    return pd.DataFrame(mat, index=names, columns=names)


def draw_graph(graph, names: list[str], title: str, path: Path) -> None:
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

    for n1, n2, e1, e2, _ in extract_edges(graph):
        a, b = shorten(pos[n1], pos[n2])
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#444", lw=1.4, zorder=1)
        for endpoint, tip, other in ((e1, a, b), (e2, b, a)):
            if endpoint.value == Endpoint.ARROW.value:
                ax.annotate(
                    "",
                    xy=tip,
                    xytext=(tip + other) / 2,
                    arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.4),
                    zorder=1,
                )
            elif endpoint.value == Endpoint.CIRCLE.value:
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


def run_test(test: str, df: pd.DataFrame, bk: BackgroundKnowledge) -> None:
    out_dir = OUT_ROOT / test
    out_dir.mkdir(parents=True, exist_ok=True)

    data = encode_for_test(df, test)

    # tell CG test which columns are categorical
    test_kwargs = {}
    if test == "cg":
        test_kwargs["discrete_cols"] = [VARIABLES.index(c) for c in DISCRETE]
    n_used = f"{data.shape[0]:,}"
    print(f"\n--- {test} --- {n_used} rows")

    print("PC...")
    cg = pc(
        data,
        ALPHA,
        test,
        stable=True,
        background_knowledge=bk,
        node_names=VARIABLES,
        show_progress=False,
        verbose=False,
        **test_kwargs,
    )
    pc_edges = extract_edges(cg.G)
    adjacency_frame(cg.G, VARIABLES).to_csv(out_dir / "pc_adjacency.csv")
    (out_dir / "pc_edges.txt").write_text("\n".join(l for *_, l in pc_edges) + "\n")
    draw_graph(cg.G, VARIABLES, f"PC -- {test}", out_dir / "pc_graph.png")

    print("FCI...")
    g, _ = fci(
        data,
        test,
        ALPHA,
        background_knowledge=bk,
        node_names=VARIABLES,
        show_progress=False,
        verbose=False,
        **test_kwargs,
    )
    fci_edges = extract_edges(g)
    adjacency_frame(g, VARIABLES).to_csv(out_dir / "fci_adjacency.csv")
    (out_dir / "fci_edges.txt").write_text("\n".join(l for *_, l in fci_edges) + "\n")
    draw_graph(g, VARIABLES, f"FCI (PAG) -- {test}", out_dir / "fci_graph.png")

    print(f"PC: {len(pc_edges)} edges, FCI: {len(fci_edges)} edges")


def main() -> None:
    bk = build_background_knowledge()

    df = pd.read_csv(DATA_PATH, usecols=VARIABLES)[VARIABLES].copy()
    for test in TESTS:
        run_test(test, df, bk)

    print("\nDone.")


if __name__ == "__main__":
    main()
