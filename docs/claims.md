# Claims

1. Switching between robot skills in contact can impose a measurable physical hysteresis cost.
2. Instantaneous reward-based switching can over-switch even when the better policy is known.
3. A hysteresis-aware supervisor can reduce switch count and physical displacement at the same task reward in a toy contact simulation.
4. The key hidden assumption broken is that switching is mechanically free or memoryless.
5. V2 shows the tradeoff: hysteresis+dwell reduces mean switch cost from 171.0 to 29.5 across 50 seeds, but mean tracking error rises from 0.090 to 0.186.
6. Over-hysteresis is a failure mode: it reduces switch cost to 11.4 but raises mean error to 0.439.
