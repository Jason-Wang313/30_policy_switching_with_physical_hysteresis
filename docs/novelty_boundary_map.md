# Novelty Boundary Map

## Already covered
- Hysteresis as a switching device to suppress chatter.
- Dwell-time logic as a generic hybrid safeguard.
- Policy switching among multiple learned controllers.

## Not yet covered by the strongest prior work
- Modeling the switch itself as a physical contact event with measurable relocation cost.
- Treating the cost as stateful, accumulated, and asymmetric.
- Demonstrating that a threshold calibrated only on instantaneous reward can oscillate into extra physical work.

## Hidden assumptions to break
1. Switching is computationally free.
2. Only the active policy matters, not the switch path.
3. Contact-state reset cost is negligible.
4. The better policy is always worth switching to immediately.
5. Switching cost is symmetric.
6. Switch penalties are memoryless.
7. Dwell time alone captures physical cost.
8. Hysteresis only suppresses sensor noise, not physical transients.
9. The same switch threshold works across contact phases.
10. The supervisor need not observe wear / reseating / force transients.
11. Contact geometry is static during switching.
12. Reward and physical cost are aligned.
13. A single switch cost suffices for all tasks.
14. No cost is incurred when reverting to a prior skill.
15. Policy ordering does not matter.
16. Local minima are the only switching danger.
17. Latent compliance is irrelevant.
18. Time lost during switch is just latency, not mechanics.
19. Contact transients do not compound.
20. Hysteresis can be tuned once and reused.
