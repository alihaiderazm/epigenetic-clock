"""Step 1: download the raw GEO data and the published clock weights.

Run:  .venv\\Scripts\\python.exe -I scripts\\01_download_data.py
Files that already exist are skipped, so the script is safe to re-run.
"""
from pathlib import Path
import shutil
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
WEIGHTS = ROOT / "data" / "clock_weights"

DOWNLOADS = {
    # GSE40279 (Hannum et al. 2013): 656 whole-blood samples, Illumina 450K, beta values + age/sex/ethnicity
    RAW / "GSE40279_series_matrix.txt.gz":
        "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE40nnn/GSE40279/matrix/GSE40279_series_matrix.txt.gz",
    # Published clock coefficients, mirrored as plain CSV by the biolearn project.
    # methylclockData holds the same numbers but only via Bioconductor ExperimentHub (needs R).
    WEIGHTS / "Horvath1.csv":
        "https://raw.githubusercontent.com/bio-learn/biolearn/HEAD/biolearn/data/Horvath1.csv",
    WEIGHTS / "Hannum.csv":
        "https://raw.githubusercontent.com/bio-learn/biolearn/HEAD/biolearn/data/Hannum.csv",
}


def download(url: str, target: Path) -> None:
    if target.exists() and target.stat().st_size > 0:
        print(f"skip  {target.name} (already {target.stat().st_size / 1e6:.1f} MB)")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".part")
    print(f"get   {url}")
    with urllib.request.urlopen(url) as resp, open(tmp, "wb") as out:
        shutil.copyfileobj(resp, out, length=1 << 20)
    tmp.replace(target)
    print(f"done  {target.name} ({target.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    for path, url in DOWNLOADS.items():
        download(url, path)
