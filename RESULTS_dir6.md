# Direction 6 - adenoma signal (preregistered in PREREG_dir3_9.md, "Direction 6"; src/dir6.py; results/dir6.json)
(a) ADA vs CTR, leave-one-cohort-out over the 4 cohorts with adenomas: AT 0.500, FR 0.477, IT 0.526, US-2 0.547. Median 0.513. Gate (>=0.65): FAIL.
(b) CRC-trained model scoring ADA vs CTR: AT 0.521, FR 0.564, IT 0.444, US-2 0.496. Median 0.509. Gate (>=0.60): FAIL.
Median scores per cohort order CTR < CRC strongly, but ADA sits at the CTR level (e.g. AT: CTR 0.308, ADA 0.304, CRC 0.750). Honest negative: with this model and these cohorts, adenomas carry no detectable species-level signal. Small n (ADA 15-47 per cohort).


> CHRONOLOGY CAVEAT (added 2026-10-10): the prereg-before-scoring order cannot be verified from git history. PREREG and results were committed in the same commits (98e4d15, 4dfe993, 7dd19ae, ae557bd, about 4 minutes apart on 10-08, author-set dates), and the 'Direction 6/10 added before scoring' notes are self-reported inside those result commits. Read the gates as author-stated, not verified preregistration. Wording correction only; no numbers or JSON changed.
