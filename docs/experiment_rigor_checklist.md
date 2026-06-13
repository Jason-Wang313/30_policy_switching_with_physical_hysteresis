# Experiment Rigor Checklist

- [x] Main simulator is `scripts/run_switch_hysteresis_sim.py`.
- [x] Main figure regenerates as `figures/switch_hysteresis_sim.png`.
- [x] Baseline comparison includes immediate switching.
- [x] V2 supervisor stress includes immediate, dwell-only, deadband-only, hysteresis+dwell, and over-hysteresis settings.
- [x] V2 reports both switch cost and tracking error.
- [x] Negative boundary is explicit: over-hysteresis reduces switch cost to 11.4 but raises mean error to 0.439.
- [ ] No hardware validation.
- [ ] No high-fidelity contact simulator.
- [ ] No measured force/work traces.
- [ ] No tuned MPC or hybrid-control baseline.

Decision: mechanism evidence only; terminal state is workshop-only / strong-revise.
