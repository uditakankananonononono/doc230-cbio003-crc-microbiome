# Results - directions 1 and 2 (run on a 2-CPU box, 7 s total)
Protocol in PREREG_dir1_dir2.md (written before scoring). Raw numbers: results/dir1_dir2.json. Code: src/dir12.py.
Within-cohort 10x5-fold CV AUROC: AT 0.896, CN 0.859, FR 0.828, JP 0.792, DE 0.784, IT-2 0.694, US 0.675, IT 0.494, US-2 0.478. Median 0.784. Gate (>=0.70): PASS.
Leave-one-cohort-out AUROC: CN 0.880, AT 0.875, DE 0.861, JP 0.831, IT 0.812, FR 0.802, IT-2 0.772, US 0.747, US-2 0.594. Median 0.812, min 0.594. Gate (median>=0.70 and none <0.60): FAIL by the min clause (US-CRC-2 0.594).
Reading: pooled training generalises better than the small cohorts do alone (IT, US-2 are ~0.5 within-cohort at n=53/56, i.e. too small for 1,300+ features). One fixed model, no tuning. This replicates the published pattern (Wirbel 2019); it is not a novel finding.
Limits: no batch/confound correction (dir 3), fixed C=0.1, species-level mOTUs2 only, CTR vs CRC only.


> CHRONOLOGY CAVEAT (added 2026-10-10): the prereg-before-scoring order cannot be verified from git history. PREREG and results were committed in the same commits (98e4d15, 4dfe993, 7dd19ae, ae557bd, about 4 minutes apart on 10-08, author-set dates), and the 'Direction 6/10 added before scoring' notes are self-reported inside those result commits. Read the gates as author-stated, not verified preregistration. Wording correction only; no numbers or JSON changed.
