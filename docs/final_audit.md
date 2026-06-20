# Final Audit

1. Chosen thesis: Policy switching in physical contact should account for path-dependent physical switch work and transient risk, not merely instantaneous policy preference.

2. Field assumption broken: The v3 paper challenges the assumption that switching is physically free, memoryless, or purely computational.

3. New central mechanism: A stateful switch-cost-aware supervisor that treats a skill transition as a physical event with work, settling, directionality, and transient risk.

4. Genuine novelty boundary: The gate itself overlaps with dwell, deadband, hysteresis, and hybrid-control supervision. The defended contribution is the accounting objective: task error, physical switch work, and transient risk must be reported together.

5. Closest hostile prior work: Chatter-free policy switching, timer-based hybrid supervisors, generic hysteresis switching control, dwell-time logic, MPC switching penalties, and safe-RL policy switching wrappers. These make broad algorithmic novelty weak; they do not remove the physical-cost accounting claim.

6. Literature coverage: `docs/related_work_matrix.csv` has 4678 Crossref-derived sweep rows. The generated docs record 300 skim candidates, 250 deep-read candidates, and 100 hostile prior papers. OpenAlex was rate-limited and Crossref recovery was used.

7. Proof/formal-claim status: No formal theorem. Claims are mechanistic and empirical, supported by a large RAM-light synthetic suite plus preserved v1/v2 artifacts.

8. Strongest v3 evidence: The full-scale suite represents 8,064,000 step decisions over 7 dynamics families, 10 regimes, 12 supervisors, and 40 seeds. Immediate greedy switching has mean switch work 108.0 and mean error 0.015; calibrated cost supervision cuts mean switch work to 16.2 with mean error 0.067; oracle cost-aware supervision has best mean utility 0.034.

9. Negative controls and failures: Sticky policy achieves zero switching but fails task error. Over-hysteresis cuts switch work to 2.4 but raises mean error to 0.581. Smooth free-switch controls check that suppression should not be rewarded when switching is cheap.

10. Biggest remaining weakness: No real robot validation, no measured force/work/reseating signal, and no tuned hardware MPC baseline. The manuscript is honest about this limitation and includes a concrete hardware evaluation template.

11. Paper-readiness judgment: v3 is final for this batch pass as a full-scale synthetic/mechanism paper. It is not a hardware-validated main-track robotics claim.

12. Exact Downloads PDF path: `C:/Users/wangz/Downloads/30.pdf` (exists, size=599452 bytes, 25 pages, SHA256 `7E5EE91CFFDF20D624023BABEA90FE68BB500C32C2BD6846118A7EABCD57DEB0`). Build status: `complete`; copied flag: `True`.

13. GitHub URL: `https://github.com/Jason-Wang313/30_policy_switching_with_physical_hysteresis`.

14. Local repo PDF copy: absent after the final build script removed transient `main.pdf`.

15. PDF text markers verified: `v3 final full-scale`, `8,064,000`, `physical hysteresis`, `108.0`, and `oracle cost-aware`.
16. VLA-style visual check: link page 4 was rendered with `pdftoppm` and inspected; one-point red internal reference boxes are crisp, aligned, and no cyan boxes appear.

Additional audit notes:
- The build used `scripts/build_pdf.ps1` and removed transient `main.pdf`.
- V3 outputs are in `results/full_scale/`.
- Legacy v2 outputs remain as provenance in `results/supervisor_stress.csv` and `results/supervisor_stress_table.tex`.
