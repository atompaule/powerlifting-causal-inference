import io
import sys
import urllib.request
import zipfile
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
BULK_ZIP_URL = (
    "https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip"
)

RAW_GLOBS = ("raw-*.csv", "openpowerlifting-*.csv")


def find_existing_raw() -> Path | None:
    for pattern in RAW_GLOBS:
        matches = sorted(DATA_DIR.glob(pattern))
        if matches:
            return matches[0]
    return None


def download_with_progress(url: str) -> bytes:
    print(f"Downloading {url}")
    with urllib.request.urlopen(url) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        chunks = []
        read = 0
        while True:
            chunk = resp.read(1 << 20)  # 1 MiB
            if not chunk:
                break
            chunks.append(chunk)
            read += len(chunk)
            if total:
                pct = 100 * read / total
                print(
                    f"\r  {read / 1e6:7.1f} / {total / 1e6:.1f} MB ({pct:4.1f}%)",
                    end="",
                    flush=True,
                )
            else:
                print(f"\r  {read / 1e6:7.1f} MB", end="", flush=True)
    print()
    return b"".join(chunks)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    existing = find_existing_raw()
    if existing is not None:
        print(f"Raw dataset already exists: {existing.relative_to(DATA_DIR.parent)}")
        print("Done.")
        return

    payload = download_with_progress(BULK_ZIP_URL)

    print("Extracting CSV...")
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        csv_members = [n for n in zf.namelist() if n.endswith(".csv")]
        if not csv_members:
            sys.exit("No CSV found inside the download")
        member = csv_members[0]
        out_name = Path(member).name  # e.g. openpowerlifting-2026-05-16-<hash>.csv
        out_path = DATA_DIR / out_name
        with zf.open(member) as src, open(out_path, "wb") as dst:
            while True:
                block = src.read(1 << 20)
                if not block:
                    break
                dst.write(block)

    size_mb = out_path.stat().st_size / 1e6
    print(f"Done: {out_path.relative_to(DATA_DIR.parent)} ({size_mb:.0f} MB)")


if __name__ == "__main__":
    main()
