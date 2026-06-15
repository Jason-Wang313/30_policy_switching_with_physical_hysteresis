# Claims

1. Switching between robot skills in contact can impose path-dependent physical work and transient risk.
2. Instantaneous reward-based switching can over-switch even when the locally preferred policy is known.
3. Switch count alone is insufficient: direction, contact state, work, settling, and transient risk can change the decision.
4. Generic dwell and deadband baselines reduce chatter, but they do not by themselves account for stateful physical switch cost.
5. In the v3 full-scale suite, immediate greedy switching has mean switch work 108.0 and mean tracking error 0.015.
6. In the v3 full-scale suite, calibrated cost supervision reduces mean switch work to 16.2 with mean tracking error 0.067.
7. The oracle cost-aware supervisor achieves the best mean utility, 0.034, showing the value of accurate switch-cost estimates.
8. Over-hysteresis is a failure mode: it reduces switch work to 2.4 but raises mean error to 0.581.
9. The supported conclusion is physical switch-cost accounting, not universal dominance of one threshold rule.
10. The paper does not claim hardware validation; the next required upgrade is measured robot switch work, force transients, and settling loss.
