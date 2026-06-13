# Submission Attack Log

Updated: 2026-06-13

## Attack Rounds

1. Closest-prior attack: hybrid control, dwell-time supervision, and hysteresis gates already suppress chatter. Response: keep novelty to physical switch-path cost in contact, not the gate itself.
2. Evidence attack: the main run is a toy simulation with no hardware. Response: keep paper-readiness workshop-only.
3. Tuned-baseline attack: a dwell or deadband supervisor may explain the result. Response: add v2 supervisor stress with immediate, dwell-only, deadband-only, hysteresis+dwell, and over-hysteresis settings.
4. Tradeoff attack: switch suppression may just worsen tracking. Response: v2 reports tracking error alongside switch cost.
5. Artifact attack: v1 left `main.pdf` locally and copied a Desktop PDF. Response: build script copies only to Downloads and removes local PDF; Desktop copy is removed.

## V2 Outcome

The paper remains workshop-only / strong-revise. Hysteresis+dwell cuts mean switch cost from 171.0 to 29.5, but raises mean tracking error from 0.090 to 0.186. The supported claim is switch-cost accounting, not universal performance improvement.
