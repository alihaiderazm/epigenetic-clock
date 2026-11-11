"""Step 6: static PNG charts of the Phase I results (for the README, slides and video).

Run:  .venv\\Scripts\\python.exe -I scripts\\06_make_figures.py
Output: figures/*.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
FIG = ROOT / "figures"

HORVATH, HANNUM = "#2a78d6", "#eb6834"
NEUTRAL, INK, INK2, MUTED, GRID, SURFACE = "#c3c2b7", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
COLORS = {"Horvath": HORVATH, "Hannum": HANNUM}
BIG_ERROR = 8

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 12,
    "axes.edgecolor": NEUTRAL, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.8, "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.labelcolor": INK2,
})


def save(fig, name):
    fig.savefig(FIG / name, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def pred_vs_real(d):
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), sharey=True)
    for ax, clock in zip(axes, ["Horvath", "Hannum"]):
        p = d[f"{clock.lower()}_pred"]
        big = (p - d.age).abs() > BIG_ERROR
        ax.fill_between([10, 110], [10 - BIG_ERROR, 110 - BIG_ERROR], [10 + BIG_ERROR, 110 + BIG_ERROR], color=GRID, alpha=.6, lw=0)
        ax.plot([10, 110], [10, 110], ls="--", color=MUTED, lw=1.5)
        ax.scatter(d.age[~big], p[~big], s=16, color=NEUTRAL, edgecolor=SURFACE, lw=.5, label=f"within {BIG_ERROR} y")
        ax.scatter(d.age[big], p[big], s=22, color=COLORS[clock], edgecolor=SURFACE, lw=.5, label=f"off by > {BIG_ERROR} y ({big.mean():.0%})")
        mae = (p - d.age).abs().mean()
        ax.set_title(f"{clock}: MAE {mae:.1f} y, bias {(p - d.age).mean():+.1f} y")
        ax.set_xlim(10, 110); ax.set_ylim(10, 110); ax.set_aspect("equal")
        ax.set_xlabel("Real (chronological) age")
        ax.legend(loc="upper left")
    axes[0].set_ylabel("Predicted age")
    fig.suptitle("Where is the clock wrong? Predicted vs. real age, GSE40279 (n = 656)", x=.07, ha="left", fontsize=16, fontweight="bold", color=INK)
    save(fig, "fig1_predicted_vs_real.png")


def residual_by_age(d):
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.axhline(0, color=NEUTRAL, lw=2)
    for clock in ["Horvath", "Hannum"]:
        r = d[f"{clock.lower()}_residual"]
        ax.scatter(d.age, r, s=10, color=COLORS[clock], alpha=.18, lw=0)
        b = d.assign(r=r, band=(d.age // 5) * 5).groupby("band").r.agg(["mean", "size"]).query("size >= 5")
        ax.plot(b.index + 2.5, b["mean"], color=COLORS[clock], lw=2.5, marker="o", ms=6, mec=SURFACE, mew=1.5)
        ax.annotate(clock, (b.index[-1] + 2.5, b["mean"].iloc[-1]), xytext=(8, 0), textcoords="offset points", va="center", color=INK2)
        slope = np.polyfit(d.age, r, 1)[0] * 10
        ax.plot([], [], color=COLORS[clock], lw=2.5, label=f"{clock}: mean per 5-y band ({slope:+.1f} y per decade)")
    ax.set_ylim(-30, 30)
    ax.set_xlabel("Real age"); ax.set_ylabel("Residual = predicted − real (years)")
    ax.set_title("Both clocks lose ~2 years per decade: young people are over-, old people under-estimated")
    ax.legend(loc="lower left")
    save(fig, "fig2_residual_by_age.png")


def mae_by_band(s):
    t = s.query("group_by == 'age_band'")
    order = ["<40", "40-49", "50-59", "60-69", "70-79", "80+"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    x = np.arange(len(order)); w = .38
    for i, clock in enumerate(["Horvath", "Hannum"]):
        g = t[t.clock == clock].set_index("group").loc[order]
        for ax, col in zip(axes, ["mae", "bias_mean_residual"]):
            bars = ax.bar(x + (i - .5) * w, g[col], w - .04, color=COLORS[clock], label=clock)
            ax.bar_label(bars, fmt="%+.1f" if col != "mae" else "%.1f", padding=3, fontsize=9, color=INK2)
    for ax, title in zip(axes, ["Mean absolute error (years)", "Bias = mean residual (years)"]):
        ax.set_xticks(x, order); ax.set_xlabel("Age band"); ax.set_title(title); ax.grid(axis="x", visible=False)
    axes[1].axhline(0, color=NEUTRAL, lw=1.5)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", ncol=2, bbox_to_anchor=(1, 1.06))
    fig.suptitle("Error per age band", x=.07, y=1.04, ha="left", fontsize=16, fontweight="bold", color=INK)
    save(fig, "fig3_error_by_age_band.png")


def perturbation(p):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), sharey=True)
    for clock in ["Horvath", "Hannum"]:
        n = p[(p.clock == clock) & (p.drop_frac == 0)]
        m = p[(p.clock == clock) & (p.noise_sd == 0)]
        axes[0].plot(n.noise_sd, n.mae, color=COLORS[clock], lw=2.5, marker="o", ms=6, mec=SURFACE, mew=1.5, label=clock)
        axes[1].plot(m.drop_frac * 100, m.mae, color=COLORS[clock], lw=2.5, marker="o", ms=6, mec=SURFACE, mew=1.5, label=clock)
    axes[0].axvspan(0.01, 0.02, color=GRID, alpha=.8, lw=0)
    axes[0].text(0.015, 1, "typical\narray noise", ha="center", color=INK2, fontsize=10)
    axes[0].set_xlabel("Gaussian noise added to every beta value (SD)")
    axes[1].set_xlabel("CpGs missing, replaced by CpG median (%)")
    axes[0].set_ylabel("Mean absolute error (years)")
    axes[0].set_title("Measurement noise"); axes[1].set_title("Missing CpGs")
    axes[0].set_ylim(0, None); axes[0].legend(loc="upper left")
    fig.suptitle("How stable are the predictions? (mean of 20 random draws per setting)", x=.07, ha="left", fontsize=16, fontweight="bold", color=INK)
    save(fig, "fig4_perturbation_stability.png")


def plate_effect(d):
    plates = sorted(d.plate.unique())
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={"width_ratios": [1, 1.3]})
    a = d.groupby("plate").age.mean().loc[plates]
    hisp = d.groupby("plate").ethnicity.agg(lambda s: (s == "Hispanic - Mexican").mean()).loc[plates]
    bars = axes[0].bar([str(p) for p in plates], a, color=[NEUTRAL if h == 0 else INK2 for h in hisp])
    axes[0].bar_label(bars, fmt="%.0f", padding=3, fontsize=9, color=INK2)
    axes[0].set_title("Mean age per plate (dark = Hispanic plates)")
    axes[0].set_xlabel("Plate"); axes[0].set_ylabel("Mean real age"); axes[0].grid(axis="x", visible=False)
    x = np.arange(len(plates)); w = .38
    for i, clock in enumerate(["Horvath", "Hannum"]):
        v = d.groupby("plate")[f"{clock.lower()}_age_accel_resid"].mean().loc[plates]
        axes[1].bar(x + (i - .5) * w, v, w - .04, color=COLORS[clock], label=clock)
    axes[1].axhline(0, color=NEUTRAL, lw=1.5)
    axes[1].set_xticks(x, [str(p) for p in plates]); axes[1].set_xlabel("Plate"); axes[1].grid(axis="x", visible=False)
    axes[1].set_ylabel("Age-adjusted residual (years)")
    axes[1].set_title("After removing the age trend: ±3 y batch effect")
    axes[1].legend(loc="lower left")
    save(fig, "fig5_plate_batch_effect.png")


def main():
    FIG.mkdir(exist_ok=True)
    d = pd.read_csv(PROC / "clock_predictions.csv")
    pred_vs_real(d)
    residual_by_age(d)
    mae_by_band(pd.read_csv(PROC / "summary_metrics.csv"))
    perturbation(pd.read_csv(PROC / "perturbation_results.csv"))
    plate_effect(d)


if __name__ == "__main__":
    main()
