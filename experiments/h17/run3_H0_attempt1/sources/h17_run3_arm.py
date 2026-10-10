"""Registered GS250 experiment; the adopted Fly remains unchanged.

Only q is new instance policy memory. Diagnostics are returned by the pure
schedule function for an external recorder, never attached to the agent.
"""
import numpy as np
from fly import Fly, angdiff

S_ON = 250
L0 = 30
GAMMA = 15.0
HALF_PERIOD = 150


def schedule(q_pre, whiffs, h, cast_sign, base_tgt, est, base_turn, enabled=True):
    q = np.where(np.asarray(whiffs).any(1), 0, np.asarray(q_pre, dtype=np.int64) + 1)
    eligible = (q >= S_ON) & (h == -1)
    engaged = eligible & bool(enabled)
    u = np.where(engaged, q - S_ON, -1).astype(np.int64)
    k = np.ones(q.shape, np.int64)
    while np.any(engaged & (u >= L0*k*(k+1)//2)):
        k += (engaged & (u >= L0*k*(k+1)//2)).astype(np.int64)
    leg = np.where(engaged, k, 0).astype(np.int64)
    remaining = np.where(engaged, L0*k*(k+1)//2-u, 0).astype(np.int64)
    sigma = np.where(engaged, cast_sign*np.where(k % 2 == 1, 1, -1), 0).astype(np.int8)
    alpha = np.where(engaged, np.where(u % (2*HALF_PERIOD) < HALF_PERIOD, 1, -1), 0).astype(np.int8)
    base_clip = np.clip(0.6*angdiff(base_tgt, est), -40.0, 40.0)
    residual = base_turn - base_clip
    target = (180.0 + sigma*(90.0-alpha*GAMMA)) % 360.0
    search_clip = np.clip(0.6*angdiff(target, est), -40.0, 40.0)
    search_turn = search_clip + residual
    return dict(q_pre=np.asarray(q_pre, dtype=np.int64).copy(), q_post=q, eligible=eligible,
                engaged=engaged, u=u, leg=leg, remaining=remaining, sigma=sigma, alpha=alpha,
                BASE_TGT=base_tgt.copy(), BASE_TURN=base_turn.copy(), BASE_CLIP=base_clip,
                RESIDUAL=residual, SEARCH_TGT=np.where(engaged, target, base_tgt),
                SEARCH_CLIP=np.where(engaged, search_clip, base_clip),
                SEARCH_TURN=np.where(engaged, search_turn, base_turn))


class GS250(Fly):
    SEARCH_ENABLED = True

    def __init__(self, runs, rng, known, nch=2, rng3=None):
        if nch != 2:
            raise ValueError('GS250 is registered at two channels only')
        super().__init__(runs, rng, known, nch=nch, rng3=rng3)
        self.q = np.zeros(runs, np.int64)

    def act(self, w, whiffs, wind_on):
        turn, h = Fly.act(self, w, whiffs, wind_on)
        d = schedule(self.q, whiffs, h, self.cast_sign, self.tgt, self.est, turn,
                     enabled=type(self).SEARCH_ENABLED)
        self.q = d['q_post']
        if d['engaged'].any():
            self.tgt = d['SEARCH_TGT']
            self.last_turn = d['SEARCH_TURN']
            turn = self.last_turn
        return turn, h


class GSOff(GS250):
    SEARCH_ENABLED = False
