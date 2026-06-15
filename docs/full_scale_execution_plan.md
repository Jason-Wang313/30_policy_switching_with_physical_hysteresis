# Paper 30 Full-Scale Execution Plan

## Current State

- Paper: `30_policy_switching_with_physical_hysteresis`
- Layout: root-level `main.tex`, not `paper/main.tex`.
- Current manuscript: compact v2 paper with a toy contact simulation and a 50-seed supervisor tuning stress.
- Current evidence:
  - Immediate switching chatters heavily in one toy trajectory.
  - Hysteresis+dwell reduces mean switch cost from 171.0 to 29.5 across 50 seeds.
  - Hysteresis+dwell raises mean tracking error from 0.090 to 0.186.
  - Over-hysteresis reduces switch cost to 11.4 but raises mean error to 0.439.
- Current weakness:
  - No real robot or high-fidelity simulator.
  - Only one toy dynamic family.
  - No broad disturbance/contact-regime sweep.
  - No calibrated physical switch-cost model.
  - No strong hybrid-control baselines beyond immediate/dwell/deadband.
  - No Pareto frontier, phase diagram, safety/risk metric, or model-mismatch stress.
  - Current docs are v2/workshop-only and stale relative to the desired final state.

## Target Standard

The final version must be a genuine full-scale formal/synthetic mechanism paper of at least 25 pages, with length earned through real new content:

- Larger hybrid/contact switching simulations.
- Many seeds, regimes, baselines, and stress tests.
- Stronger supervisors and calibrated objective tradeoffs.
- Negative controls where hysteresis is unnecessary or harmful.
- Failure cases and sensitivity analysis.
- Figures/tables generated from compact reproducible outputs.
- Clear no-real-robot boundary and a concrete hardware follow-up protocol.

The final PDF should be exported only when complete to `C:\Users\wangz\Downloads\30.pdf`, with local `main.pdf` removed afterward.

## Experiment Design

### Dynamics Families

Implement a RAM-light full-scale runner that evaluates multiple finite/synthetic physical switching worlds:

- Boundary tracking with noisy mode preference.
- Stick-slip contact with reseating cost.
- Gripper recontact with transient settling.
- Locomotion foothold phase switching with lost-progress cost.
- Hybrid force/position control around contact onset.
- Object pushing with surface-dependent mode hysteresis.
- Negative-control smooth dynamics where switching is almost free.

### Regimes

Evaluate at least:

- Low noise / low physical switch cost.
- High noise / low physical switch cost.
- Low noise / high physical switch cost.
- High noise / high physical switch cost.
- Asymmetric switch costs.
- Delayed settling after switch.
- Nonstationary target or contact boundary drift.
- Model-mismatch switch-cost estimates.
- Free-switch negative control.
- Over-hysteresis failure regime.

### Baselines and Methods

Evaluate:

- Immediate greedy switching.
- Fixed dwell only.
- Deadband only.
- Hysteresis+dwell.
- Over-hysteresis.
- Switch-penalty greedy objective.
- Adaptive hysteresis tuned online from observed switch work.
- Cost-calibrated supervisor using estimated physical switch cost.
- Risk-aware supervisor that penalizes force/transient overshoot.
- Oracle cost-aware supervisor with true switch cost.
- No-switch or sticky-policy baseline.
- Randomized debounce baseline.

### Metrics

Report:

- Switch count.
- Accumulated physical switch work.
- Tracking error.
- Final error.
- Settling time.
- Force/transient overshoot.
- Chatter episodes.
- Utility = task error plus weighted switch cost.
- Pareto dominance and Pareto gap.
- Regret relative to oracle cost-aware supervisor.
- Safety violation rate.
- Coverage of regimes where hysteresis helps, hurts, or is neutral.

## RAM-Light Execution Strategy

- Use only Python standard library if possible; avoid matplotlib dependency for v3 core outputs.
- Use streaming aggregate counters rather than raw per-step logs.
- Write compact CSV/JSON summaries.
- Generate simple PDF figures with a minimal standard-library renderer, or keep existing PNG only as legacy.
- Run seeds sequentially.
- Keep per-regime state arrays out of memory except for short representative traces.
- Store exact run scale and validation metadata.

## Manuscript Rewrite Plan

The final manuscript should be rewritten around v3 evidence:

1. Abstract with exact v3 scale and the central tradeoff.
2. Introduction: switching as physical event, not a free computation.
3. Related work: hybrid systems, hysteresis/dwell, safe RL switching, contact-rich robot skill libraries, force/position switching.
4. Formal problem setup:
   - mode state;
   - physical switch cost;
   - path dependence;
   - dwell and hysteresis as special cases;
   - objective with task error, switch work, transient risk.
5. Supervisor families and baselines.
6. Full-scale synthetic setup:
   - dynamics families;
   - regimes;
   - metrics;
   - seed counts;
   - RAM-light implementation.
7. Results:
   - main aggregate performance;
   - Pareto frontier;
   - phase diagram over switch cost/noise;
   - model-mismatch stress;
   - asymmetric costs;
   - negative controls;
   - over-hysteresis failure.
8. Discussion:
   - when hysteresis helps;
   - when it hurts;
   - why dwell alone is not enough;
   - how to measure real switch cost.
9. Limitations:
   - no hardware;
   - synthetic dynamics;
   - simplified costs;
   - need real force/work/reseating data.
10. Appendices:
   - algorithm details;
   - metric derivations;
   - full tables;
   - real robot protocol;
   - failure catalog;
   - reviewer attack responses.

## Figures and Tables

Required final artifacts:

- Scale table.
- Main performance table by method.
- Dynamics-family table.
- Pareto frontier table or figure.
- Phase diagram figure.
- Model-mismatch table.
- Negative-control table.
- Over-hysteresis/failure table.
- Representative trace figure.
- Appendix table with full method/regime metrics.

## Documentation Updates

After final export:

- Update `README.md`.
- Update `child_status.md`.
- Update `docs/final_audit.md`.
- Update `docs/claims.md`.
- Update `docs/experiment_rigor_checklist.md`.
- Update `docs/reproducibility_checklist.md`.
- Update `docs/submission_readiness_decision.md`.
- Update `docs/submission_version_log.md`.
- Update `docs/hostile_reviewer_response.md`.
- Update `docs/reviewer_attacks.md`.
- Update `docs/submission_attack_log.md`.
- Add/update `results/full_scale/README.md` and validation JSON.

## Final Acceptance Checklist

- Full-scale runner completes from repo root.
- New results are compact and reproducible.
- Manuscript is at least 25 pages.
- Manuscript has clear v3 final marker and exact scale numbers.
- Final build log is clean for fatal errors, unresolved references/citations, and overfull boxes.
- Final PDF is copied only to `C:\Users\wangz\Downloads\30.pdf`.
- Local `main.pdf` is removed after final export.
- PDF text markers verify it is the v3 final full-scale paper.
- Docs match final results and final PDF hash.
- Git commit is pushed.
- Worktree is clean and local `HEAD` equals upstream before moving to Paper31.
