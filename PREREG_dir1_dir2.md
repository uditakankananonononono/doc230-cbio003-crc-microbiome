# Preregistration - CBIO003 (2023-2026 ISEF list) directions 1 and 2
Written before any model was scored.
Data: Wirbel 2019 meta-analysis (mOTUs2, g2_l75), 9 CRC cohorts, CTR vs CRC only. Hashes in data_manifest/SHA256.txt.
Model: L1-regularised logistic regression (C=0.1 fixed, not tuned), features = species with max rel. abundance >=1e-3 in training data, log10(x+1e-5) then per-feature standardise (fit on train only). Seed 0.
Dir 1 (within-cohort): 10x repeated 5-fold CV per cohort, report mean AUROC. Gate: pooled-median AUROC >= 0.70 = baseline replicates.
Dir 2 (cross-cohort): leave-one-cohort-out (train 8, test 1). Gate: median LOCO AUROC >= 0.70 and no cohort < 0.60 counts as generalising; report all.
Comparator: majority/dummy AUROC 0.5. No tuning on test cohorts. Negative outcomes are reported as is.
Limits: single model family; mOTUs2 species profiles only; cohort effects not corrected (that is dir 3).
