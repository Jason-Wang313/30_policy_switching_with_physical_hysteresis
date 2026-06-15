# Submission Attack Log

Updated: 2026-06-15

## Attack Rounds

1. Closest-prior attack: hybrid control, dwell-time supervision, and hysteresis gates already suppress chatter. Response: keep novelty to physical switch-path cost in contact, not the gate itself.
2. Evidence attack: the original run was a toy simulation with no hardware. Response: v3 adds a broader synthetic suite but keeps hardware claims out of scope.
3. Tuned-baseline attack: dwell or deadband may explain the result. Response: v3 includes immediate greedy, dwell-only, deadband-only, hysteresis+dwell, fixed penalty, adaptive, calibrated, risk-aware, oracle, sticky, and randomized baselines.
4. Tradeoff attack: switch suppression may just worsen tracking. Response: v3 reports task error, switch work, transient risk, utility, and win rate together.
5. Fewer-switches attack: suppressing all switches can look good on switching metrics. Response: v3 includes sticky-policy failure and over-hysteresis trap.
6. Cheap-switch attack: a method should not suppress switches when switching is physically cheap. Response: v3 includes a smooth free-switch control.
7. Calibration attack: calibrated cost may fail under model mismatch. Response: v3 includes model-mismatch and oracle comparisons.
8. Artifact attack: final PDFs must live only in Downloads after completion. Response: `scripts/build_pdf.ps1` copies to `C:/Users/wangz/Downloads/30.pdf` and removes local `main.pdf`.

## V3 Outcome

The paper is final for this batch pass as a full-scale synthetic/mechanism paper. It is 25 pages, uses 8,064,000 represented step decisions, and preserves honest limitations around missing hardware validation.
