"""Step 3: apply the published Horvath and Hannum clocks in Python and evaluate them (Phase I).

Replaces the methylclock R step (R is not installed); the formulas are the published ones:
  Hannum : age = sum_i w_i * beta_i                      (71 CpGs, no intercept)
  Horvath: age = anti_trafo(0.695507258 + sum_i w_i * beta_i)   (353 CpGs)
           anti_trafo(x) = 21 * exp(x) - 1   if x < 0
                           21 * x + 20       otherwise

Outputs (data/processed/):
  clock_predictions.csv   one row per person: real age, both predictions, residuals, age acceleration
  summary_metrics.csv     MAE, median AE, r, bias per clock and group (all / sex / ethnicity / age band)
  perturbation_results.csv  how predictions move under measurement noise and missing CpGs (RQ2)
  imputation_report.csv   which CpG values were imputed
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
WEIGHTS = ROOT / "data" / "clock_weights"

HORVATH_INTERCEPT = 0.695507258  # Horvath 2013, Additional file 3
ADULT_AGE = 20
BIG_ERROR_YEARS = 8
AGE_BANDS = [0, 40, 50, 60, 70, 80, 200]
AGE_BAND_LABELS = ["<40", "40-49", "50-59", "60-69", "70-79", "80+"]
RNG_SEED = 40279


def anti_trafo(x):
    return np.where(x < 0, (1 + ADULT_AGE) * np.exp(x) - 1, (1 + ADULT_AGE) * x + ADULT_AGE)


def load_weights() -> dict[str, pd.Series]:
    out = {}
    for clock, file in [("Horvath", "Horvath1.csv"), ("Hannum", "Hannum.csv")]:
        w = pd.read_csv(WEIGHTS / file).set_index("CpGmarker")["CoefficientTraining"]
        out[clock] = w
    return out


def predict(clock: str, weights: pd.Series, betas: np.ndarray) -> np.ndarray:
    """betas: (n_cpgs, n_samples) in the same order as weights."""
    s = weights.values @ betas
    return anti_trafo(s + HORVATH_INTERCEPT) if clock == "Horvath" else s


def metrics(age: np.ndarray, pred: np.ndarray) -> dict:
    err = pred - age
    return {
        "n": len(age),
        "mae": np.mean(np.abs(err)),
        "median_ae": np.median(np.abs(err)),
        "r": np.corrcoef(age, pred)[0, 1] if len(age) > 2 else np.nan,
        "bias_mean_residual": np.mean(err),
        "share_err_gt_8y": np.mean(np.abs(err) > BIG_ERROR_YEARS),
    }


def main() -> None:
    samples = pd.read_csv(PROC / "samples.csv")
    betas_df = pd.read_csv(PROC / "clock_cpg_betas.csv", index_col="cpg")[samples.sample_id]
    weights = load_weights()

    # --- imputation: missing single values -> median of that CpG across all people.
    # (methylclock imputes too; we use the simple median variant and log every imputed cell.)
    missing = betas_df.isna()
    imp_report = (missing.sum(axis=1).rename("n_imputed_values").reset_index()
                  .query("n_imputed_values > 0"))
    imp_report.to_csv(PROC / "imputation_report.csv", index=False)
    medians = betas_df.median(axis=1)
    betas_df = betas_df.T.fillna(medians).T

    age = samples.age.to_numpy(float)
    pred_df = samples.copy()
    clock_betas = {}
    for clock, w in weights.items():
        present = w.index.intersection(betas_df.index)
        if len(present) < len(w):
            print(f"WARNING {clock}: {len(w) - len(present)} CpGs absent from data, dropped")
        w = w.loc[present]
        weights[clock] = w
        b = betas_df.loc[present].to_numpy(float)
        clock_betas[clock] = b
        p = predict(clock, w, b)
        key = clock.lower()
        pred_df[f"{key}_pred"] = p
        pred_df[f"{key}_residual"] = p - age  # 'age acceleration' in the simple difference sense
        slope, intercept = np.polyfit(age, p, 1)
        pred_df[f"{key}_age_accel_resid"] = p - (slope * age + intercept)  # residual-based AgeAccel
    pred_df["age_band"] = pd.cut(pred_df.age, AGE_BANDS, right=False, labels=AGE_BAND_LABELS)
    pred_df.round(4).to_csv(PROC / "clock_predictions.csv", index=False)

    # --- group metrics
    rows = []
    for clock in weights:
        p = pred_df[f"{clock.lower()}_pred"].to_numpy()
        rows.append({"clock": clock, "group_by": "all", "group": "all", **metrics(age, p)})
        for col in ["sex", "ethnicity", "age_band", "plate"]:
            for g, idx in pred_df.groupby(col, observed=True).groups.items():
                i = pred_df.index.get_indexer(idx)
                rows.append({"clock": clock, "group_by": col, "group": g, **metrics(age[i], p[i])})
    summary = pd.DataFrame(rows)
    summary.round(3).to_csv(PROC / "summary_metrics.csv", index=False)

    # --- perturbation (RQ2): Gaussian noise on beta values, and randomly 'lost' CpGs replaced by
    #     the CpG median (what an imputing pipeline would do). 20 repeats per setting.
    rng = np.random.default_rng(RNG_SEED)
    pert = []
    for clock, w in weights.items():
        b = clock_betas[clock]
        base = predict(clock, w, b)
        med = medians.loc[w.index].to_numpy()[:, None]
        for noise_sd in [0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1]:
            for drop_frac in [0, 0.05, 0.1, 0.2, 0.3, 0.5]:
                for rep in range(20 if (noise_sd or drop_frac) else 1):
                    bb = np.clip(b + rng.normal(0, noise_sd, b.shape), 0, 1) if noise_sd else b.copy()
                    if drop_frac:
                        drop = rng.random(len(w)) < drop_frac
                        bb[drop] = np.broadcast_to(med[drop], bb[drop].shape)
                    p = predict(clock, w, bb)
                    pert.append({"clock": clock, "noise_sd": noise_sd, "drop_frac": drop_frac,
                                 "rep": rep, "mae": np.mean(np.abs(p - age)),
                                 "bias": np.mean(p - age),
                                 "mean_abs_shift": np.mean(np.abs(p - base)),
                                 "r": np.corrcoef(age, p)[0, 1]})
    pert = (pd.DataFrame(pert).groupby(["clock", "noise_sd", "drop_frac"])
            .agg(mae=("mae", "mean"), mae_sd=("mae", "std"), bias=("bias", "mean"),
                 mean_abs_shift=("mean_abs_shift", "mean"), r=("r", "mean")).reset_index())
    pert.round(4).to_csv(PROC / "perturbation_results.csv", index=False)

    # --- console summary
    print(f"imputed values: {int(missing.values.sum())} cells in {len(imp_report)} CpGs")
    pd.set_option("display.width", 160)
    print(summary.round(2).to_string(index=False))
    print(pert.query("drop_frac == 0 or noise_sd == 0").round(2).to_string(index=False))


if __name__ == "__main__":
    main()
