# Reviewer Attacks

1. This is dwell-time, deadband, or hysteresis gating rebranded.
2. The suite is synthetic, not a robot.
3. Physical hysteresis cost is not measured on hardware.
4. A tuned MPC or hybrid-control baseline may match the result.
5. The novelty might collapse into generic switching penalties.
6. Hysteresis may trade lower switch work for worse tracking.
7. Fewer switches are not necessarily better.
8. The calibrated supervisor may only work when the switch-cost model is correct.

## Responses

- Emphasize stateful, path-dependent physical switch-cost accounting rather than the gate itself.
- Be explicit that the evidence is synthetic and mechanistic, not hardware validation.
- Report task error, switch count, switch work, transient risk, utility, and win rate together.
- Use the v3 baselines: immediate greedy, dwell-only, deadband-only, hysteresis+dwell, over-hysteresis, switch-penalty greedy, adaptive hysteresis, calibrated cost, risk-aware, oracle cost, sticky policy, and randomized debounce.
- Use negative controls: smooth free-switch control, sticky-policy failure, and over-hysteresis trap.
- Concede that hardware validation is the next step and provide the exact hardware evaluation template.
