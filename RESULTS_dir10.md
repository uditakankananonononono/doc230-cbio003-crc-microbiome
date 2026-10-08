# Direction 10 - functional (KEGG) vs species (PREREG_dir3_9.md "Direction 10"; src/dir10.py; results/dir10.json)
Only 8 of 9 cohorts have KEGG profiles (US-CRC-2 absent). Same LR, same samples.
(a) LOCO within 5 discovery cohorts, species vs KEGG AUROC: AT .845/.723, CN .861/.831, DE .916/.819, FR .827/.835, US .729/.804. Medians 0.845 vs 0.819.
(b) Train on 5 discovery, test on externals: IT .806/.710, IT-2 .780/.703, JP .814/.782. Medians 0.806 vs 0.710.
Gate (KEGG >= species +0.02 in both): FAIL. Function features did not beat species; only US and FR favoured KEGG. Note species numbers differ from dir 2 because training here is restricted to 5 cohorts.
Limits: KEGG from the published pipeline, no tuning, 3 external cohorts.
