# Hold D0: scope of the counter-bound reading (2026-10-09)

Code review identified this limitation independently of D0 results, while the local passive measurement was running. No quantity, criterion, sample, seed or implementation changed. The registered FINAL remains unchanged.

The preserved v1 section 3.1 universal claim over any world or horizon is not a theorem. The selection circuit adds Gaussian noise with unbounded support, and the strict deterministic decay inequality fails at zero. D0 reports counter margins and formation/release observations in its registered fixed sample. A PASS of observed window checks supports those measured conditions only; it cannot prove that a rare noise-driven late formation is impossible at an arbitrary horizon. Not building a two-channel condition is an engineering recommendation under an approximate bound, not a general impossibility result.

Source: src/fly.py, selection circuit step, Gaussian noise and feedback update; notes/hold/2026-10-07-hold-branch-exposure-design-v1.md section 3.1. Reports must state this scope and distinguish observations from the bound's assumptions.
