#!/usr/bin/env python3
"""Development-seed diagnosis of A1(b)'s failure (side balance) in the H20 dev run. Measurement only.

The dev run reached the -y source first in 94 percent of neutral-arm rows. Suspected cause: the
adopted agent's initial cast side is the same for every row (ph11.Agent: cast_sign = +1), so every
agent's first cast swing from the midline goes to the same side. Checked here by running the
neutral arm (values 0/0, so the gain is inert) with the initial cast side as adopted, flipped for
every row, and drawn per row. Nothing in ph16.py is changed; the initial state is set after
construction, as a world would set a heading.
"""
import hashlib
import numpy as np
import ph16
from ph16 import SEEDS, outcome, diagnostics

MODES = {"adopted (+1 all rows)": lambda n, rng: np.ones(n), "flipped (-1 all rows)": lambda n, rng: -np.ones(n),
         "drawn per row": lambda n, rng: rng.choice([1.0, -1.0], n)}
_init = ph16.Agent4.__init__


def main():
    print(f"== A1(b) diagnosis on the development seeds {SEEDS['dev']}. this file sha256 "
          f"{hashlib.sha256(open(__file__, 'rb').read()).hexdigest()} ==")
    for name, fn in MODES.items():
        def patched(self, runs, rng, **kw):
            _init(self, runs, rng, **kw); self.cast_sign = fn(runs, rng)
        ph16.Agent4.__init__ = patched
        o = ph16.run("neutral", SEEDS["dev"], 2.0); V, N, Z = outcome(o); d = diagnostics(o); m = d["reached"]
        k = int(((d["which"] == o["plus_y"]) & m).sum()); fh_plus = int(((d["fh"] == o["plus_y"]) & (d["fh"] >= 0)).sum())
        print(f"   initial cast side {name:22s}: reached +y first {k}/{int(m.sum())} = {k/m.sum():.3f}; no-choice {int(Z.sum())};"
              f" first hold on the +y odour {fh_plus}/{int((d['fh'] >= 0).sum())}; first-approach step median {ph16.med(d['rs'][m]):.0f}")
    ph16.Agent4.__init__ = _init


if __name__ == "__main__":
    main()
