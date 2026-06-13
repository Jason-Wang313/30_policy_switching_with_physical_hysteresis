# Reproducibility Checklist

- [x] Main simulator is `scripts/run_switch_hysteresis_sim.py`.
- [x] Build script is `scripts/build_pdf.ps1`.
- [x] Main figure is `figures/switch_hysteresis_sim.png`.
- [x] V2 outputs are `results/supervisor_stress.csv` and `results/supervisor_stress_table.tex`.
- [x] Paper source is `main.tex`.
- [x] Canonical PDF path is `C:/Users/wangz/Downloads/30.pdf`.
- [x] Local `main.pdf` is removed after canonical copy.
- [x] Visible Desktop PDF copies are absent.

Recommended verification commands:

```powershell
python scripts\run_switch_hysteresis_sim.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```
