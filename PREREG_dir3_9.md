# Preregistration - directions 3,4,5,7,8,9 (written before scoring; same data/model as dir1-2 unless stated)
Dir3 confound audit: (a) predict Study label from CTR-only samples (multinomial LR, 5-fold CV, accuracy vs majority); (b) per-cohort standardisation (z-score features within each cohort) then LOCO. Gate: (a) accuracy > 2x majority-share = strong cohort signal; (b) counts as helpful if LOCO median AUROC rises >= 0.02.
Dir4 minimal panel: within each LOCO training fold rank species by |L1 coef| from full model, take top k in {5,10,20,50}, refit, test on held-out cohort. Gate: smallest k with median LOCO AUROC >= (full median - 0.02).
Dir5 known taxa: Fusobacterium nucleatum, Parvimonas micra, Peptostreptococcus stomatis, Gemella morbillorum, Solobacterium moorei, Porphyromonas asaccharolytica (matched by name substring in mOTUs names). Per-cohort Wilcoxon CRC vs CTR, direction and BH-FDR; gate: taxon replicates if enriched in CRC in >=7/9 cohorts with same sign.
Dir7 transforms: LOCO with (i) log10 rel abund (baseline), (ii) raw rel abund, (iii) presence/absence (>=1e-3), (iv) CLR with pseudocount 1e-5. Report medians; no winner threshold, descriptive.
Dir8 calibration/screening: pooled LOCO predictions; report specificity at 90% sensitivity per cohort and pooled Brier score before/after nothing (no recalibration). Descriptive.
Dir9 covariates: on cohorts with complete Age,Gender,BMI, LOCO AUROC of covariates-only LR vs microbiome-only vs combined. Gate: microbiome adds >=0.03 AUROC over covariates-only.

# Direction 6 (added before scoring, 2026-10-08)
Cohorts with adenoma (ADA) labels: AT-CRC, FR-CRC, IT-CRC, US-CRC-2. (a) ADA vs CTR leave-one-cohort-out among these 4 (same LR). Gate: median AUROC >= 0.65. (b) Score ADA vs CTR with the CRC-vs-CTR model trained on the other 8 cohorts (no ADA seen); gate median >= 0.60. Descriptive: score ordering CTR < ADA < CRC median per cohort.

# Direction 10 (added before scoring)
KEGG ortholog profiles from the same Zenodo record: discovery file (5 cohorts AT, CN, DE, FR, US) and external file (IT, IT-2, JP, US-2). Same LR (L1, C=0.1, log10 rel. abundance after row-sum normalisation, features with max >=1e-4 in training; species threshold 1e-3). Compare with species on the SAME samples. (a) LOCO within the 5 discovery cohorts, KEGG vs species. (b) Train on the 5 discovery cohorts, test on each external CTR/CRC cohort. Gate: function counts as better only if median AUROC exceeds species by >=0.02 in both (a) and (b).
