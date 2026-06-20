# Child Status: Paper 30

Stage: complete; v3 final full-scale hardening ready to commit and push

Current facts:
- Literature sweep completed with `docs/related_work_matrix.csv` containing 4678 Crossref-derived rows.
- Original toy simulator and v2 stress artifacts are preserved for provenance.
- A paper-specific full-scale execution plan was written before substantive v3 edits at `docs/full_scale_execution_plan.md`.
- Full-scale suite is `scripts/run_full_scale_hysteresis_suite.py`.
- Full-scale outputs are in `results/full_scale/`.
- The v3 suite covers 7 families, 10 regimes, 12 methods, 40 seeds, 240 steps per seed, and 8,064,000 represented step decisions.
- Main v3 result: immediate greedy switching has mean switch work 108.0 and mean error 0.015; calibrated cost supervision has mean switch work 16.2 and mean error 0.067; oracle cost-aware supervision has best mean utility 0.034.
- Negative controls remain explicit: sticky policy fails on task error, over-hysteresis traps reduce switch work but raise mean error to 0.581, and the smooth free-switch control checks that cheap switches should not be suppressed.
- Paper source is `main.tex` with visible `v3 final full-scale` marker and 25 rendered pages.
- Canonical final PDF is `C:/Users/wangz/Downloads/30.pdf` with SHA256 `7E5EE91CFFDF20D624023BABEA90FE68BB500C32C2BD6846118A7EABCD57DEB0`.
- Final PDF size is 599452 bytes.
- Latest visual hardening: VLA-style one-point red internal link boxes verified on page 4; green cite/url border policy configured, with no cite/url annotations present in this manuscript.
- Transient `main.pdf` was removed by `scripts/build_pdf.ps1`.
- Public GitHub repo exists: `https://github.com/Jason-Wang313/30_policy_switching_with_physical_hysteresis`.

Commands run:
- `python scripts\run_full_scale_hysteresis_suite.py`
- `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice for local page-count QA
- `powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1`
- Safe probes for build status, Downloads PDF, local PDF absence, LaTeX log status, PDF text markers, page count, file size, and SHA256 hash.

Historical failures:
- Original attempts failed on optional `mutool`, LaTeX style path issues, and natbib-sensitive bibliography entries.
- V1 was manually recovered before prior hardening.
- V2 was useful but short and toy-scale; v3 replaces it with a broader full-scale synthetic manuscript.

Next:
- Commit and push the v3 hardening update.
