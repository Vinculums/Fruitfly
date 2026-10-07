"""Passive local read-out projection; no counterfactual is fed into the next tick.

Only hr and hold_projection are added to Fly. The original act performs every
state update and random draw. Passivity is a replay gate, not an assumed result.
"""
import numpy as np
import fly

MEASUREMENT_ATTRIBUTES = frozenset({'hr', 'hold_projection'})


class PassiveFly(fly.Fly):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hr = np.full(self.R, -1)
        self.hold_projection = None

    def act(self, w, whiffs, wind_on):
        hp = self.held().copy()
        since = self.since.copy()
        silence = self.silence.copy()
        result = super().act(w, whiffs, wind_on)
        _, h = result
        rows = np.arange(self.R)
        v = self.chan_valence()
        # Reconstruct precisely Upstream.step's returned value from its already
        # updated P; do not call step again or modify the upstream object.
        u = self.up
        others = (u.P.sum(1, keepdims=True) - u.P) / max(u.P.shape[1] - 1, 1)
        y = u.Rmax * u.P / (u.sig_n + u.P + u.k * others)
        y = y * (1.0 + self.G * np.maximum(v, 0.0))
        vh = v[rows, np.maximum(hp, 0)]
        y = y * ~((hp >= 0)[:, None] & (v >= 0.0) & (v < vh[:, None]))
        self.hr = np.where(y.max(1) > 0.05, y.argmax(1), -1)
        reset_silence = np.where(self.due_timeout | self.due_evidence, 0.0, silence)
        reference = self._project(h, whiffs, since, reset_silence)
        alternative = self._project(self.hr, whiffs, since, reset_silence)
        # N2 still uses actual hp/h and actual-held whiffs, not the projection.
        new = (h >= 0) & (h != hp)
        negz = (h >= 0) & (v[rows, np.maximum(h, 0)] < 0.0)
        newz = new & ~negz
        for projection in (reference, alternative):
            projection['post_silence'] = np.where(
                self.sustain, fly.RESET_AFTER + 1.0,
                np.where(newz, 0.0, projection['silence']))
        self.hold_projection = dict(y=y, H=reference, R=alternative,
                                    release=(self.due_timeout | self.due_evidence).copy())
        return result

    def _project(self, identity, whiffs, since, silence):
        rows = np.arange(self.R)
        index = np.maximum(identity, 0)
        v = self.chan_valence()
        val = np.where(identity >= 0, self.known[rows, index], 0.0)
        hit = np.where(identity >= 0, whiffs[rows, index], False)
        vh = v[rows, index]
        held = np.zeros_like(whiffs)
        held[rows, index] = identity >= 0
        present = (self.c < self.N) | held
        vmax = np.where(present, v, -np.inf).max(1)
        top = present & (v >= 0) & (v == vmax[:, None])
        if self.nch == 3:
            nT = top.sum(1)
            bT = np.where(top, self.bb, -np.inf).max(1)
            ranked = top & (self.bb == bT[:, None]) & (bT > fly.NEVER)[:, None]
            eligible = np.where((nT >= 2)[:, None], ranked, top)
            keep = (identity >= 0) & (eligible[rows, index] | (vh < 0))
        else:
            eligible = top
            keep = (identity >= 0) & ((vh == vmax) | (vh < 0))
        nav = np.where(keep, hit, (whiffs & eligible).any(1))
        next_since = np.where(nav, 0.0, since + 1.0)
        next_silence = np.where(hit, 0.0, silence + 1.0)
        side = np.where((next_since // fly.CAST_PERIOD) % 2 == 0, 1.0, -1.0) * self.cast_sign
        off = fly.MAXOFF * (1.0 - np.abs((next_since / fly.SAT) % 2.0 - 1.0))
        tgt = np.where(nav, fly.UPWIND, (fly.UPWIND + side * off) % 360.0)
        tgt = np.where(val < 0, self.flee_side, tgt)
        clipped = np.clip(fly.GAIN * fly.angdiff(tgt, self.est), -fly.MAXTURN, fly.MAXTURN)
        return dict(identity=identity.copy(), val=val, hit=hit, vh=vh,
                    presence_override=held, presence=present, top=top, eligible=eligible,
                    keep=keep, nav=nav, since=next_since, silence=next_silence,
                    flee=val < 0, tgt=tgt, clipped_turn=clipped)
