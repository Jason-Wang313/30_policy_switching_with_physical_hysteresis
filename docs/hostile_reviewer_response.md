# Hostile Reviewer Response

## Likely Rejection

This is still dwell-time, hysteresis, or switching-penalty control under another name. The experiments are synthetic, and some methods reduce switch work by accepting worse tracking.

## Honest Response

The criticism is partly correct. The paper should not sell the gate itself as the novelty. The defended contribution is the accounting: in contact-rich robotics, switching can be a physical event with path-dependent work, settling loss, and transient risk. The evaluation should therefore report task error, switch work, and risk together.

The v3 suite makes this sharper than v2. Across 8,064,000 represented step decisions, immediate greedy switching has mean switch work 108.0 and mean error 0.015. Calibrated cost supervision lowers mean switch work to 16.2 with mean error 0.067. Oracle cost-aware supervision gives the best utility, 0.034. Over-hysteresis is explicitly shown as a failure, with mean error 0.581. The paper claims physical switch-cost accounting, not free improvement and not universal superiority of one threshold.

## Required Upgrade For Main-Track Hardware Submission

- Measure physical switch work, force transients, and reseating loss on hardware.
- Compare against tuned dwell-only, deadband-only, switching-penalty, MPC, and hybrid-control baselines.
- Learn or estimate switch costs from contact traces.
- Optimize a calibrated objective over task error, switch work, settling time, and transient risk.
