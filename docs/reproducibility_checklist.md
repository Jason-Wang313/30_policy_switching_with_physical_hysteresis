# Reproducibility Checklist

- [x] Full-scale runner is `scripts/run_full_scale_hysteresis_suite.py`.
- [x] Build script is `scripts/build_pdf.ps1`.
- [x] Paper source is `main.tex`.
- [x] Full-scale CSV outputs are in `results/full_scale/seed_metrics.csv` and `results/full_scale/aggregate_metrics.csv`.
- [x] Full-scale summary is `results/full_scale/experiment_summary.json`.
- [x] Generated manuscript tables are in `results/full_scale/*.tex`.
- [x] Generated v3 figures are in `figures/full_scale/`.
- [x] Legacy figure is `figures/switch_hysteresis_sim.png`.
- [x] Canonical PDF path is `C:/Users/wangz/Downloads/30.pdf`.
- [x] Canonical PDF is 25 pages and 599452 bytes.
- [x] Canonical PDF SHA256 is `7E5EE91CFFDF20D624023BABEA90FE68BB500C32C2BD6846118A7EABCD57DEB0`.
- [x] Local `main.pdf` is removed after canonical copy.
- [x] `build_pdflatex2.log` has no overfull boxes, unresolved references, undefined citations, fatal errors, or TeX `!` errors.
- [x] VLA-style link-box policy is configured in `main.tex`; final PDF has one-point red internal reference boxes and no cyan boxes.

Recommended verification commands:

```powershell
python scripts\run_full_scale_hysteresis_suite.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
pdfinfo C:\Users\wangz\Downloads\30.pdf
Get-FileHash -Algorithm SHA256 C:\Users\wangz\Downloads\30.pdf
Test-Path main.pdf
```
