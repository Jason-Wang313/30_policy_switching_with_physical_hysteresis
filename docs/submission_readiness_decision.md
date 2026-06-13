# Submission Readiness Decision

Decision: workshop-only / strong-revise.

## Why Not Submit-Ready

- Evidence is a toy simulator, not a real robot or mature contact model.
- The supervisor is close to generic hysteresis/dwell control.
- V2 shows switch suppression increases tracking error.
- There is no measured force, work, reseating, or wear signal.
- There is no calibrated optimization over task error and physical switch cost.

## Why Not Kill

- The physical-switch-cost framing is a useful contact-rich robotics lens.
- The main simulator cleanly exposes chatter and accumulated switching work.
- The v2 stress makes the tracking/switch-cost tradeoff explicit.
- The claim is now narrow enough to survive a hostile reading.

## Required Next Work

- Measure physical switch transients on a manipulation or locomotion system.
- Compare against tuned dwell/deadband/hybrid-control baselines.
- Learn switch-cost models from contact traces.
- Optimize policies over task reward, switch work, and recovery time.
