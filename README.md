Replication of the Wirbel 2019 pattern, mixed: across 9 CRC cohorts, leave-one-cohort-out AUROC median 0.812 but the dir 2 gate failed on the min clause (US-CRC-2 0.594) and the dir 3 confound-correction gate was also missed (per-cohort z-scoring +0.016 vs +0.02 required; study label predictable from controls alone, 0.854 vs 0.154 majority); adenoma (dir 6) and KEGG-vs-species (dir 10) are negative; not a novel finding.

# doc230-cbio003-crc-microbiome
ISEF CBIO003 (Colorectal cancer detection from gut microbiome) - 10 buildable directions. All 10 run (6 and 10 negative; 2 and 3 missed gates). Data: Wirbel 2019 via Zenodo (hashes in data_manifest). Run: python3 src/dir12.py (needs /tmp/meta_all.tsv, /tmp/sp.tsv).


## Provenance disclosure (added 2026-10-10) - chronology of prereg vs scoring is NOT verifiable from git history; 'before scoring' notes are self-reported
The commit chain cannot show that gates preceded results for dirs 1-2 and 3-9: PREREG and results were committed together (98e4d15, 4dfe993), and the dir 6 and dir 10 gates were added inside the result commits (7dd19ae, ae557bd). The 'added before scoring' statements in PREREG_dir3_9.md are author claims only (dates author-set). History is not rewritten. Verdicts are unchanged; misses are reported as misses.

Note: there is no single RESULTS.md; results are split across RESULTS_dir1_dir2.md, RESULTS_dir3_9.md, RESULTS_dir6.md, RESULTS_dir10.md (raw json in results/). All numbers are builder-reported, not independently rerun.
