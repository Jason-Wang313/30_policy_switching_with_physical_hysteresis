# Plan

1. Extract the actual paper text from `30.pdf` and identify the real thesis, mechanism, and experiment set.
2. Build the literature pipeline in escalating passes:
   - 1000-paper landscape sweep
   - 300-paper serious skim
   - 200-250-paper deep read
   - 100-paper hostile prior-work set
3. Write and continuously refresh the required review artifacts in `docs/`:
   - `related_work_matrix.csv`
   - `literature_map.md`
   - `hostile_prior_work.md`
   - `novelty_boundary_map.md`
   - `novelty_decision.md`
   - `claims.md`
   - `reviewer_attacks.md`
   - `final_audit.md`
4. Decide the strongest thesis only after the hostile-prior comparison, then draft the anonymous ICLR-style paper around the winning mechanism.
5. Compile the paper PDF, verify the output, copy it to `C:/Users/wangz/Downloads/30.pdf`, and document the GitHub publish state.
