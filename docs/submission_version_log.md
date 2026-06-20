# Submission Version Log

## v3 - 2026-06-15

- Wrote `docs/full_scale_execution_plan.md` before substantive v3 edits.
- Added `scripts/run_full_scale_hysteresis_suite.py`.
- Generated full-scale outputs under `results/full_scale/`.
- Generated v3 figures under `figures/full_scale/`.
- Expanded `main.tex` into a 25-page final full-scale manuscript with v3 marker, full-scale results, controls, failures, reproducibility material, hardware evaluation template, and claim-boundary appendices.
- Built the canonical PDF at `C:/Users/wangz/Downloads/30.pdf`.
- Verified the v3 final PDF hash before the later visual-hardening rebuild.
- Verified local `main.pdf` was removed by the build script.

## v4 Visual Hardening - 2026-06-20

- Added the VLA role-model `hyperref` box policy to `main.tex`.
- Rebuilt the canonical Downloads PDF.
- Verified 25 pages, size 599,452 bytes, SHA256 `7E5EE91CFFDF20D624023BABEA90FE68BB500C32C2BD6846118A7EABCD57DEB0`, and no local `main.pdf`.
- Verified one-point red internal link boxes on page 4, with no cyan boxes. The manuscript has no cite/url link annotations, so green cite/url boxes are configured but not present.

## v2 - 2026-06-13

- Added supervisor stress generation to `scripts/run_switch_hysteresis_sim.py`.
- Generated `results/supervisor_stress.csv`.
- Generated `results/supervisor_stress_table.tex`.
- Updated the manuscript with a visible v2 note, supervisor stress table, and narrowed discussion.
- Added `scripts/build_pdf.ps1` to build, copy to Downloads, and remove local `main.pdf`.

## v1 - 2026-06-11

- Recovered initial physical-hysteresis switching paper package with literature sweep, toy simulation, ICLR-style manuscript, final audit, canonical Downloads PDF, Desktop copy, and public GitHub repo.
