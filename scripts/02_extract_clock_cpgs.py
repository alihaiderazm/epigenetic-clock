"""Step 2: stream the 1.2 GB GEO series matrix and keep only what the clocks need.

Outputs (data/processed/):
  samples.csv           one row per person: GSM id, age, sex, ethnicity, plate, source
  clock_cpg_betas.csv   beta values for the Horvath + Hannum CpGs only (rows = CpGs, columns = GSM ids)
  cpg_availability.csv  per clock CpG: present in the data? how many missing values?

The full matrix (473k CpGs x 656 people) never has to fit in memory.
"""
from pathlib import Path
import gzip

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "raw" / "GSE40279_series_matrix.txt.gz"
WEIGHTS = ROOT / "data" / "clock_weights"
OUT = ROOT / "data" / "processed"


def unquote(fields):
    return [f.strip().strip('"') for f in fields]


def clock_cpgs() -> dict[str, set[str]]:
    return {
        "Horvath": set(pd.read_csv(WEIGHTS / "Horvath1.csv")["CpGmarker"]),
        "Hannum": set(pd.read_csv(WEIGHTS / "Hannum.csv")["CpGmarker"]),
    }


def parse_characteristics(lines: list[list[str]], n: int) -> dict[str, list[str]]:
    """GEO stores 'key: value' pairs, one !Sample_characteristics_ch1 line per key."""
    out: dict[str, list[str]] = {}
    for fields in lines:
        key = fields[0].split(":", 1)[0].strip()
        out[key] = [f.split(":", 1)[1].strip() if ":" in f else None for f in fields]
        assert len(out[key]) == n
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    clocks = clock_cpgs()
    wanted = set().union(*clocks.values())

    header: dict[str, list[str]] = {}
    characteristics: list[list[str]] = []
    rows: dict[str, list[str]] = {}
    n_rows = 0

    with gzip.open(MATRIX, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("!series_matrix_table_begin"):
                break
            if line.startswith("!Sample_"):
                key, *vals = line.rstrip("\n").split("\t")
                vals = unquote(vals)
                if key == "!Sample_characteristics_ch1":
                    characteristics.append(vals)
                else:
                    header[key] = vals

        columns = unquote(next(fh).rstrip("\n").split("\t"))[1:]
        for line in fh:
            if line.startswith("!series_matrix_table_end"):
                break
            n_rows += 1
            cpg, rest = line.split("\t", 1)
            cpg = cpg.strip('"')
            if cpg in wanted:
                rows[cpg] = rest.rstrip("\n").split("\t")

    ids = header["!Sample_geo_accession"]
    assert ids == columns, "sample order in header and table differ"
    ch = parse_characteristics(characteristics, len(ids))

    samples = pd.DataFrame({
        "sample_id": ids,
        "title": header["!Sample_title"],
        "age": pd.to_numeric(ch["age (y)"]),
        "sex": ch["gender"],
        "ethnicity": ch["ethnicity"],
        "plate": ch["plate"],
        "source": ch["source"],
    })
    samples.to_csv(OUT / "samples.csv", index=False)

    betas = pd.DataFrame.from_dict(rows, orient="index", columns=ids)
    betas = betas.apply(pd.to_numeric, errors="coerce")  # GEO writes missing values as "null"/empty
    betas.index.name = "cpg"
    betas.sort_index().to_csv(OUT / "clock_cpg_betas.csv")

    avail = []
    for clock, cpgs in clocks.items():
        for cpg in sorted(cpgs):
            present = cpg in betas.index
            avail.append({
                "clock": clock,
                "cpg": cpg,
                "present_in_data": present,
                "n_missing_values": int(betas.loc[cpg].isna().sum()) if present else len(ids),
            })
    avail = pd.DataFrame(avail)
    avail.to_csv(OUT / "cpg_availability.csv", index=False)

    print(f"matrix rows scanned : {n_rows:,}")
    print(f"samples             : {len(samples)}")
    print(f"clock CpGs kept     : {len(betas)} of {len(wanted)} wanted")
    for clock, g in avail.groupby("clock"):
        print(f"  {clock:8s} absent CpGs: {(~g.present_in_data).sum():3d}   "
              f"CpGs with some missing values: {((g.n_missing_values > 0) & g.present_in_data).sum()}")
    print(f"beta range          : {np.nanmin(betas.values):.3f} .. {np.nanmax(betas.values):.3f}")
    print(samples.describe(include="all").T[["count", "unique", "top", "mean", "min", "max"]])


if __name__ == "__main__":
    main()
