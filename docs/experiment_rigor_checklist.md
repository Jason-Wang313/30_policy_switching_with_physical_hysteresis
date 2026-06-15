# Experiment Rigor Checklist

- [x] A paper-specific v3 execution plan was written before substantive full-scale edits.
- [x] Full-scale runner is `scripts/run_full_scale_hysteresis_suite.py`.
- [x] Full-scale suite covers 7 dynamics families and 10 stress/control regimes.
- [x] Full-scale suite compares 12 supervisors.
- [x] Full-scale suite uses 40 seeds and 8,064,000 represented step decisions.
- [x] Baselines include immediate greedy, dwell-only, deadband-only, hysteresis+dwell, over-hysteresis, fixed switch penalty, adaptive hysteresis, calibrated cost supervision, risk-aware supervision, oracle cost supervision, sticky policy, and randomized debounce.
- [x] Metrics include switch count, switch work, tracking error, transient risk, utility, and win rate.
- [x] Negative controls are explicit: sticky policy, over-hysteresis trap, and smooth free-switch control.
- [x] Figures include work-by-method, error/work Pareto, and regime-winner phase views.
- [x] Tables include scale, main performance, family summary, regime winners, and controls/failures.
- [x] Legacy toy/v2 artifacts are preserved for provenance.
- [ ] No hardware validation.
- [ ] No measured force/work traces.
- [ ] No tuned hardware MPC or hybrid-control baseline.

Decision: final for the batch pass as a full-scale synthetic/mechanism paper; hardware claims remain out of scope.
