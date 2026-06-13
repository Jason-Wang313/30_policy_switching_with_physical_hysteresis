# Hostile Reviewer Response

## Likely Rejection

This is just dwell-time or hysteresis gating, evaluated in a toy simulator. The supervisor reduces switching by tolerating worse tracking, so the result may be a tuning artifact rather than a new robotics insight.

## Honest Response

We agree that the gate itself is not novel. The intended contribution is the accounting: in contact, switching can be a physical event with path-dependent work and reseating cost.

The v2 stress quantifies the tradeoff. Across 50 seeds, immediate switching has mean switch cost 171.0 and mean error 0.090. Hysteresis+dwell lowers switch cost to 29.5 but increases mean error to 0.186. Over-hysteresis lowers switch cost further to 11.4 but raises mean error to 0.439. The paper should claim calibrated switch-cost accounting, not broad dominance.

## Required Upgrade For Main-Track Submission

- Measure physical switch work, force transients, and reseating loss on hardware.
- Compare against tuned dwell-only, deadband-only, MPC, and hybrid-control baselines.
- Learn or estimate switch costs from contact traces.
- Optimize a calibrated objective over task error and physical switch cost.
