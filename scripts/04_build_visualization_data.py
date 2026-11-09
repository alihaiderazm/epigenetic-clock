"""Step 4: package the processed data into visualization/data.js for the interactive view.

The browser needs the raw clock-CpG betas and weights (not only the predictions) so the noise /
missing-CpG sliders can recompute both clocks live, exactly like 03_compute_clocks.py does.
"""
from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
WEIGHTS = ROOT / "data" / "clock_weights"
OUT = ROOT / "visualization" / "data.js"


def main() -> None:
    pred = pd.read_csv(PROC / "clock_predictions.csv")
    betas = pd.read_csv(PROC / "clock_cpg_betas.csv", index_col="cpg")[pred.sample_id]
    betas = betas.T.fillna(betas.median(axis=1)).T  # same median imputation as step 3
    pert = pd.read_csv(PROC / "perturbation_results.csv")

    weights = {}
    for clock, file in [("Horvath", "Horvath1.csv"), ("Hannum", "Hannum.csv")]:
        w = pd.read_csv(WEIGHTS / file).set_index("CpGmarker")["CoefficientTraining"]
        w = w.loc[w.index.intersection(betas.index)]
        weights[clock] = {"cpgs": list(w.index), "w": [float(x) for x in w.values]}

    payload = {
        "dataset": "GSE40279",
        "horvathIntercept": 0.695507258,
        "samples": [
            {"id": r.sample_id, "age": r.age, "sex": r.sex, "ethnicity": r.ethnicity,
             "plate": str(r.plate), "Horvath": round(r.horvath_pred, 2), "Hannum": round(r.hannum_pred, 2)}
            for r in pred.itertuples()
        ],
        "weights": weights,
        "betas": {cpg: [round(float(v), 4) for v in row] for cpg, row in betas.iterrows()},
        "medians": {cpg: round(float(v), 4) for cpg, v in betas.median(axis=1).items()},
        "perturbation": pert.round(3).to_dict(orient="records"),
    }
    OUT.write_text("window.CLOCK_DATA = " + json.dumps(payload, separators=(",", ":")) + ";\n",
                   encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.2f} MB), {len(payload['samples'])} samples, "
          f"{len(payload['betas'])} CpGs")


if __name__ == "__main__":
    main()
