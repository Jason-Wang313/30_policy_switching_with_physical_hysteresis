# Final Audit

1. Chosen thesis: Policy switching in physical contact should account for a hysteretic physical switch cost.

2. Field assumption broken: The run challenges the assumption that switching is physically free, memoryless, or purely computational.

3. New central mechanism: A stateful switch-cost-aware supervisor that treats a skill transition as a physical event with path-dependent work, force transient, and reseating loss.

4. Genuine novelty: The paper is not a new policy library or benchmark. Its novelty is modeling the switch path itself as part of the contact-control objective.

5. Closest hostile prior work: Chatter-free policy switching, timer-based hybrid supervisors, generic hysteresis switching control, dwell-time logic, and safe-RL policy switching wrappers. These make the gate less novel; the remaining claim is physical switch-cost accounting.

6. Literature coverage: `docs/related_work_matrix.csv` has 4678 Crossref-derived sweep rows. The generated docs record 300 skim candidates, 250 deep-read candidates, and 100 hostile prior papers. OpenAlex was rate-limited and Crossref recovery was used.

7. Proof/formal-claim status: No formal theorem. Claims are mechanistic and empirical, supported by a toy simulation and a v2 stress sweep.

8. Strongest evidence: The original toy contact simulation contrasts immediate switching with hysteresis-aware gating. The immediate-switch baseline performs 224 switches and accumulates 179.2 units of switch cost, while the hysteresis-aware supervisor performs 35 switches and accumulates 28.0 units of switch cost.

9. V2 stress evidence: Across 50 seeds, immediate switching has mean switch cost 171.0 and mean tracking error 0.090. Hysteresis+dwell lowers switch cost to 29.5 but raises mean error to 0.186. Over-hysteresis lowers switch cost to 11.4 but raises mean error to 0.439. This supports switch-cost accounting, not free performance improvement.

10. Biggest weaknesses: No hardware validation; toy simulator only; novelty may be incremental relative to hybrid control; no measured force/work/reseating signal; no calibrated optimization over tracking error and physical switch cost.

11. Paper-readiness judgment: workshop-only / strong-revise. The mechanism is useful, but a strong ICLR submission would need robot measurements, tuned hybrid-control baselines, and learned/calibrated switch-cost models.

12. Exact Downloads PDF path: `C:/Users/wangz/Downloads/30.pdf` (exists, size=345672 bytes). Build status: `complete`; copied flag: `True`.

13. GitHub URL: `https://github.com/Jason-Wang313/30_policy_switching_with_physical_hysteresis`.

14. Visible Desktop PDF copy: absent at checked Desktop paths (expected; canonical PDF is Downloads only).

15. Local repo PDF copy: absent (expected after Downloads copy).

Additional audit notes:
- The build used `scripts/build_pdf.ps1` and removed transient `main.pdf`.
- V2 outputs are `results/supervisor_stress.csv` and `results/supervisor_stress_table.tex`.
