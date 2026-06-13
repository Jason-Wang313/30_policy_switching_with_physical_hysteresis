# Child Status: Paper 30

Stage: complete; v2 submission hardening ready to commit and push

Current facts:
- Literature sweep completed with `docs/related_work_matrix.csv` containing 4678 Crossref-derived rows.
- Main toy simulator regenerated `figures/switch_hysteresis_sim.png`.
- Original headline result remains: immediate switching performs 224 switches and accumulates 179.2 switch-cost units; hysteresis-aware gating performs 35 switches and accumulates 28.0 switch-cost units.
- V2 supervisor stress generated `results/supervisor_stress.csv` and `results/supervisor_stress_table.tex`.
- V2 stress result: across 50 seeds, hysteresis+dwell cuts mean switch cost from 171.0 to 29.5 but raises mean tracking error from 0.090 to 0.186; over-hysteresis reaches 11.4 switch cost but 0.439 mean error.
- Paper source is `main.tex` with visible v2 note, supervisor stress table, and narrowed discussion.
- LaTeX build completed with `scripts/build_pdf.ps1`.
- Final PDF copied to `C:/Users/wangz/Downloads/30.pdf`.
- Transient `main.pdf` removed so the final PDF exists only at the required Downloads path.
- Checked Desktop paths contain no `30.pdf`.
- Public GitHub repo exists: `https://github.com/Jason-Wang313/30_policy_switching_with_physical_hysteresis`.
- `docs/final_audit.md` exists and reports build status, v2 stress evidence, Downloads-only artifact status, Desktop absence, and local PDF absence.

Commands run:
- `python scripts\run_switch_hysteresis_sim.py`
- `powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1`
- Safe probes for build status, Downloads PDF, Desktop absence, local PDF absence, LaTeX log status, and generated stress outputs.

Historical failures:
- Original attempts failed on optional `mutool`, LaTeX style path issues, and natbib-sensitive bibliography entries.
- V1 was manually recovered before this hardening pass.

Recovery / hardening steps:
- Added v2 supervisor stress and narrowed the claim to calibrated switch-cost accounting.
- Added standard hardening docs: attack log, version log, hostile reviewer response, rigor checklist, reproducibility checklist, and readiness decision.
- Added `scripts/build_pdf.ps1` and `.gitignore` rule for `main.pdf`.
- Rebuilt the canonical PDF and removed the tracked local PDF.

Next:
- Commit and push the v2 hardening update.
