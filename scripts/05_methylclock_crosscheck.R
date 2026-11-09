# Step 5: cross-check our Python clocks against the official methylclock R package.
# Run:  & "C:\Program Files\R\R-4.6.2\bin\Rscript.exe" scripts\05_methylclock_crosscheck.R
#
# Outputs (data/processed/):
#   methylclock_predictions.csv  methylclock's Horvath + Hannum ages per sample
#   methylclock_coefficients.csv methylclockData's coefficients (incl. intercept) for both clocks
#   crosscheck_summary.csv       Python vs methylclock: weight and prediction differences

suppressPackageStartupMessages({
  library(methylclock)
  library(methylclockData)
})

root <- normalizePath(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))), ".."))
proc <- file.path(root, "data", "processed")
wdir <- file.path(root, "data", "clock_weights")

betas <- read.csv(file.path(proc, "clock_cpg_betas.csv"), check.names = FALSE)
py <- read.csv(file.path(proc, "clock_predictions.csv"))

# --- 1. compare coefficients: methylclockData vs the biolearn CSVs used in Python
coef_mc <- list(Horvath = get_coefHorvath(), Hannum = get_coefHannum())
coef_py <- list(Horvath = read.csv(file.path(wdir, "Horvath1.csv")), Hannum = read.csv(file.path(wdir, "Hannum.csv")))

coef_rows <- list()
summary_rows <- list()
for (clock in names(coef_mc)) {
  mc <- coef_mc[[clock]]
  mc <- data.frame(cpg = mc$CpGmarker, weight = as.numeric(mc$CoefficientTraining))
  coef_rows[[clock]] <- cbind(clock = clock, mc)
  intercept <- mc$weight[mc$cpg %in% c("(Intercept)", "Intercept", "intercept")]
  mc_cpgs <- mc[!mc$cpg %in% c("(Intercept)", "Intercept", "intercept"), ]
  m <- merge(mc_cpgs, coef_py[[clock]], by.x = "cpg", by.y = "CpGmarker")
  summary_rows[[paste0(clock, "_coef")]] <- data.frame(
    clock = clock, check = "coefficients",
    detail = sprintf("methylclockData CpGs=%d, Python CpGs=%d, shared=%d, intercept=%s, max |weight diff|=%.6g",
                     nrow(mc_cpgs), nrow(coef_py[[clock]]), nrow(m),
                     ifelse(length(intercept), format(intercept, digits = 10), "none"),
                     max(abs(m$weight - m$CoefficientTraining)))
  )
}
write.csv(do.call(rbind, coef_rows), file.path(proc, "methylclock_coefficients.csv"), row.names = FALSE)

# --- 2. run methylclock itself (no normalisation, no cell counts = same input as Python)
ages <- DNAmAge(betas, clocks = c("Horvath", "Hannum"), normalize = FALSE, cell.count = FALSE)
ages <- as.data.frame(ages)
write.csv(ages, file.path(proc, "methylclock_predictions.csv"), row.names = FALSE)

m <- merge(py, ages, by.x = "sample_id", by.y = "id")
for (clock in c("Horvath", "Hannum")) {
  d <- m[[clock]] - m[[paste0(tolower(clock), "_pred")]]
  summary_rows[[paste0(clock, "_pred")]] <- data.frame(
    clock = clock, check = "predictions",
    detail = sprintf("n=%d, mean diff (methylclock - Python)=%.4f y, max |diff|=%.4f y, r=%.6f",
                     length(d), mean(d), max(abs(d)), cor(m[[clock]], m[[paste0(tolower(clock), "_pred")]]))
  )
}
summary <- do.call(rbind, summary_rows)
write.csv(summary, file.path(proc, "crosscheck_summary.csv"), row.names = FALSE)
print(summary, right = FALSE, row.names = FALSE)
