import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_PATH = Path(__file__).resolve().parent / "squat_equipment_filtered.csv"
RAW_GLOBS = ("raw-*.csv", "openpowerlifting-*.csv")

FILTERS = {
    "Event": "SBD",
    "Tested": "Yes",
    "Sanctioned": "Yes",
}

# if there is no federation entry, make it "Independent"
PARENT_FED_FALLBACK = "Independent"

# keep only these sexes (drop the ~37 "Mx" entries)
SEX_KEEP = ("M", "F")

# keep the chronologically first entry if a contestant appears more than once
DEDUP_KEEP = "first"

# final columns, in order
# Event/Tested/Sanctioned will be constant after filtering
FINAL_COLUMNS = [
    "Age",
    "BodyweightKg",
    "Sex",
    "Equipment",
    "Best3SquatKg",
    "Year",
    "ParentFederation",
    "Event",
    "Tested",
    "Sanctioned",
    "Federation",
]


def find_raw_csv() -> Path:
    for pattern in RAW_GLOBS:
        matches = sorted(DATA_DIR.glob(pattern))
        if matches:
            return matches[0]
    sys.exit(
        "No raw dataset found in data/.\n"
        "Run: python data_preprocessing/download_data.py"
    )


def log_step(label: str, df: pd.DataFrame) -> None:
    print(f"  {label:<42} {len(df):>10,} rows")


def main() -> None:
    raw_path = find_raw_csv()
    print(f"Loading {raw_path.relative_to(ROOT)} ...")

    # only work with the columns we need
    usecols = [
        "Name",
        "Sex",
        "Event",
        "Equipment",
        "Age",
        "BodyweightKg",
        "Best3SquatKg",
        "Tested",
        "Federation",
        "ParentFederation",
        "Date",
        "Sanctioned",
    ]
    df = pd.read_csv(raw_path, usecols=usecols, low_memory=False)
    log_step("raw", df)

    # derive interval-scaled Year from Date
    df["Year"] = pd.to_datetime(df["Date"], errors="coerce").dt.year

    # restrict the population
    print("Filtering population:")
    for col, value in FILTERS.items():
        df = df[df[col] == value]
        log_step(f"{col} == {value!r}", df)

    # drop the "Mx" sex (too few entries to model)
    df = df[df["Sex"].isin(SEX_KEEP)]
    log_step(f"sex in {SEX_KEEP}", df)

    # fill empty federation column with "Independent" instead of dropping the row
    df["ParentFederation"] = df["ParentFederation"].fillna(PARENT_FED_FALLBACK)

    # keep only one entry per contestant
    df = df.sort_values("Date").drop_duplicates(subset="Name", keep=DEDUP_KEEP)
    log_step(f"unique contestant (keep {DEDUP_KEEP})", df)

    # failed squats (negative weight) -> 0
    n_failed = int((df["Best3SquatKg"] < 0).sum())
    df.loc[df["Best3SquatKg"] < 0, "Best3SquatKg"] = 0
    print(f"  set {n_failed:,} failed squats (negative) -> 0")

    # keep only the variables of interest
    df = df[FINAL_COLUMNS]

    # drop all na
    df = df.dropna(axis=0, how="any")
    log_step("complete cases (dropna)", df)

    # Year is integer-valued after dropping missing dates.
    df["Year"] = df["Year"].astype(int)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(
        f"\nSaved → {OUT_PATH.relative_to(ROOT)}  ({len(df):,} rows, {df.shape[1]} cols)"
    )

    print("\nSummary:")
    print(f"  Year range          : {df['Year'].min()}–{df['Year'].max()}")
    print(
        f"  Best3SquatKg (kg)   : "
        f"min {df['Best3SquatKg'].min():.1f}, "
        f"mean {df['Best3SquatKg'].mean():.1f}, "
        f"max {df['Best3SquatKg'].max():.1f}"
    )
    print("  Equipment counts    :")
    for eq, n in df["Equipment"].value_counts().items():
        print(f"      {eq:<12} {n:>8,}")
    print("  Sex counts          :")
    for sx, n in df["Sex"].value_counts().items():
        print(f"      {sx:<12} {n:>8,}")
    print(f"  ParentFederation    : {df['ParentFederation'].nunique()} levels (top 6):")
    for pf, n in df["ParentFederation"].value_counts().head(6).items():
        print(f"      {pf:<12} {n:>8,}")
    assert df.isna().sum().sum() == 0, "missing values remain"
    assert (df["Best3SquatKg"] >= 0).all(), "negative squat remains"


if __name__ == "__main__":
    main()
