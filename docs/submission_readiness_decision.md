# Submission Readiness Decision

Decision: final for this batch pass as a v3 full-scale synthetic/mechanism paper.

## Why This Is Now Final For The Batch

- The manuscript renders to 25 pages without padding.
- The experiment scope is no longer a toy-only claim: v3 represents 8,064,000 step decisions over 7 families, 10 regimes, 12 methods, and 40 seeds.
- The paper compares generic chatter suppression, fixed penalties, calibrated supervision, risk-aware supervision, oracle supervision, sticky behavior, and randomized debounce.
- The manuscript reports the key tradeoff directly: immediate greedy switching has low error but high switch work; calibrated and oracle cost-aware supervisors reduce physical switch work and utility cost; over-hysteresis fails.
- The paper includes controls for cheap switching, over-hysteresis, model mismatch, asymmetric cost, delayed settling, and drifting boundaries.
- The final PDF exists only as the canonical Downloads artifact.

## Remaining Non-Claims

- No real robot validation.
- No measured force, work, reseating, wear, or tactile trace.
- No tuned hardware MPC or hybrid-control baseline.
- No claim that one threshold rule is universally optimal.

## Required Next Work For A Strong Hardware Submission

- Measure physical switch transients on a manipulation or locomotion system.
- Compare against tuned dwell/deadband/MPC/hybrid-control baselines.
- Learn or identify switch-cost models from contact traces.
- Optimize and report task error, switch work, settling time, risk, and utility under pre-registered weights.
