"""Navigation read-out intervention; the actual hold still drives gate/release/N2.

The inherited act wrapper returns the actual hold, even for the instant arm.
No additional random draw is made. The silence/reset coupling is intentional.
"""
import numpy as np
from fly import (Fly, RESET_AFTER, RESET_DRIVE, evidence_due, NEVER, WIN,
                 CAST_PERIOD, MAXOFF, SAT, UPWIND, GAIN, angdiff, MAXTURN,
                 TURN_NOISE)


class ReadOutFly(Fly):
    def __init__(self, *args, read='instant', **kwargs):
        if read not in ('actual', 'instant'):
            raise ValueError('read must be actual or instant')
        super().__init__(*args, **kwargs)
        self.hold_read = read == 'actual'
        self.hr = np.full(self.R, -1)

    def _act(self, w, whiffs, wind_on):
        rows = np.arange(self.R)
        y = self.up.step(whiffs.astype(float))*(1.0 + self.G*np.maximum(self.chan_valence(), 0.0))
        hp = self.held()
        v = self.chan_valence(); vh = v[rows, np.maximum(hp, 0)]
        y = y*~((hp >= 0)[:, None] & (v >= 0.0) & (v < vh[:, None]))
        self.due_timeout = self.silence > RESET_AFTER
        self.due_evidence = evidence_due(y, hp)
        due = self.due_timeout | self.due_evidence
        rst = np.where(due, RESET_DRIVE, 0.0)[:, None]
        self.silence = np.where(due, 0.0, self.silence)
        self.sel.step(y, reset=rst)
        h = self.held()
        self.hr = np.where(y.max(1) > 0.05, y.argmax(1), -1)
        hh = h if self.hold_read else self.hr
        est = self.est = self.estimate(w, wind_on)
        val = np.where(hh >= 0, self.known[rows, np.maximum(hh, 0)], 0.0)
        hit = np.where(hh >= 0, whiffs[rows, np.maximum(hh, 0)], False)
        v = self.chan_valence(); vh = v[rows, np.maximum(hh, 0)]
        if self.nch == 3:
            cp = self.c
            self.c = np.where(whiffs, 0.0, self.c + 1.0)
            t = float(self.t16)
            w1 = np.where(cp <= t - 1.0, t - 1.0 - cp, NEVER)
            self.burst = whiffs & ((t - self.w2) <= WIN)
            self.bb = np.where(self.burst, t, self.bb)
            self.w2 = np.where(whiffs, w1, self.w2)
        else:
            self.c = np.where(whiffs, 0.0, self.c + 1.0)
        held = np.zeros_like(whiffs); held[rows, np.maximum(hh, 0)] = hh >= 0
        self.present = (self.c < self.N) | held
        vmax = np.where(self.present, v, -np.inf).max(1)
        top = self.present & (v >= 0) & (v == vmax[:, None])
        if self.nch == 3:
            nT = top.sum(1); bT = np.where(top, self.bb, -np.inf).max(1)
            ranked = top & (self.bb == bT[:, None]) & (bT > NEVER)[:, None]
            topr = np.where((nT >= 2)[:, None], ranked, top)
            keep = (hh >= 0) & (topr[rows, np.maximum(hh, 0)] | (vh < 0))
            nav = np.where(keep, hit, (whiffs & topr).any(1))
        else:
            keep = (hh >= 0) & ((vh == vmax) | (vh < 0))
            nav = np.where(keep, hit, (whiffs & top).any(1))
        self.nav_hit = nav
        self.since = np.where(nav, 0.0, self.since + 1.0)
        self.silence = np.where(hit, 0.0, self.silence + 1.0)
        side = np.where((self.since // CAST_PERIOD) % 2 == 0, 1.0, -1.0)*self.cast_sign
        off = MAXOFF*(1.0 - np.abs((self.since/SAT) % 2.0 - 1.0))
        tgt = np.where(nav, UPWIND, (UPWIND + side*off) % 360.0)
        self.tgt = tgt = np.where(val < 0, self.flee_side, tgt)
        turn = np.clip(GAIN*angdiff(tgt, est), -MAXTURN, MAXTURN)
        turn = turn + TURN_NOISE*self.rng.standard_normal(self.R)
        self.last_turn = turn
        if self.nch == 3: self.t16 += 1
        return turn, h
