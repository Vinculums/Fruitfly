"""fly: the adopted agent in one file, both forms (module consolidation, design v2 FINAL).

Design: notes/module/2026-09-29-module-consolidation-design-v2.md, opened by decision:module-consolidation-open (the owner,
2026-09-29, '확정', gloss 'confirmed'). An engineering step with no hypothesis: this file is accepted only if it IS the adopted
agent bitwise (design section 6). It adds no behaviour and adopts nothing.

Forms (one constructor argument, nch):
  nch 2  Agent17 = Agent14N2 built with N_hi 200 (src/ph35.py:104-105; decision:h29-window-200-adopted-within-tested-conditions).
         The step is ph23.Agent9.act (src/ph23.py:60-104) wrapped by ph30.ReleaseN2.act (src/ph30.py:121-136).
  nch 3  Agent16 (src/ph33.py:180-194; decision:h28-burst-tie-adopted-within-tested-conditions). The step is ph33.Act16.act
         (src/ph33.py:119-177) wrapped by ReleaseN2; window 300, counter start 240, Circuit3's noise split (src/ph32.py:125-142).
Decisions implemented (as composed in the phN chain): Phase 2 stage and circuit; H19 (a); the H21 gate
(decision:h21-gate-adopted-within-tested-conditions); the H23 filter (decision:h23-filter-adopted-within-tested-conditions);
the H26 presence counter (decision:h26-adaptive-presence-adopted-within-tested-conditions); the release N2
(decision:n2-release-adopted-within-tested-conditions); the ring at tau 1 (decision:h14-adopt-tau1) fed the rotation made
(decision:heading-input-rotation-made); the return cast (decision:h16-close-limited-adoption); learning H8 v2 with the
extinction gate (decision:phase7-2-gate); for nch 3 the H27 composition rule and the H28 burst-ranked tie.

FLAG, G 2: the gain (1 + G*max(v, 0)) at G 2.0 is carried as composed in every adopted scope. Whether it is adopted state is
the owner's, unsettled (master_plan.md, consolidated record header). It is a module constant here, not a decision.

Readings recorded with this file (design v2 section 3, [v2, amendment 1]; verified by the reviewing session):
  U7  learning is credited by POSITION, not by the hold: the caller builds the code and the reinforcement from the source the
      row stands at (src/ph15.py:55-61) and calls mb.step after the move (src/ph30.py:235-238). This file keeps that.
  U8  the agent's learning module is built with K 200 (src/ph11.py:53); K 500 is the module-level constant of Phase 4 and 7.2.
  U10 the H28 tie rule is inert at two channels only for the tested value pairs (+1/0, +1/-1); at equal non-negative values
      it would act (src/ph33.py:154-158). The two-channel form therefore never runs the tie block (explicit nch == 3 branches).

Every constant is a module constant (design section 2.3; exposing one re-opens its bench). Every formed value is formed as the
phN code forms it. The random draws on the agent generator per act are, in order: circuit noise (R, 2) [then (R, 1) on rng3 at
nch 3], ring noise (R, 16) for the rotation step, ring noise (R, 16) for the cue step (when any row senses wind), turn noise (R).
Construction draws only flee_side. numpy only.
"""
import numpy as np

# ------------------------------------------------------------------ constants (design section 2.3)
# core: upstream stage (src/ph11.py:112, src/ph2.py:9)
UP_N, UP_SIG, UP_RMAX, UP_K, UP_TAU = 1.5, 0.05, 1.8, 0.8, 2.0
# core: circuit (src/ph11.py:113, src/ph2.py:23-25)
C_THETA, C_K, C_NOISE = 1.0, 12.0, 0.01
C_WI, C_G, C_TAU, C_TAUG, C_POOLP, C_POOLC = 1.0, 2.0, 10.0, 2.0, 1.0, 1.0
C_DT, C_SMAX = 1.0, 5.0
SIG_CLIP = 60                                   # ffcore.py:6
# core: hold and release (src/ph11.py:39, 144; src/ph23.py:72; src/ph24.py:62; src/ph30.py:128-129)
HOLD = 1.0
RESET_AFTER, MARGIN = 40, 0.2
RESET_DRIVE = 10.0
# core: gain (src/ph21.py:27); gate, filter, scope 'prior', release: always on
G_STAR = 2.0
# core: learning module (src/ph11.py:53, 115-116; src/ph4.py:19-20)
MB_K, MB_C, MB_SPARSITY, MB_ETA_D, MB_ETA_P, MB_BETA = 200, 4, 0.05, 0.10, 0.30, 0.15
MB_TAU_CODE, MB_TAU_REINF, MB_W0, MB_WMIN, MB_WMAX = 5.0, 5.0, 1.0, 0.0, 2.0
CODE_SEEDS = (101, 102, 103)                    # src/ph11.py:116; src/ph33.py:189
# core: presence (src/ph28.py:72, 97; src/ph35.py:89)
P_PRIOR = 60
N_HI = {2: 200, 3: 300}                         # window by form
# core: three-channel additions (src/ph33.py:105-106)
NEVER = -1.0e9
WIN = 9
# body, agent side: ring (src/ph11.py:52, 114; src/ph10.py:50) and wind cue (src/ph11.py:51; src/ph13.py:60)
RING_N, RING_NOISE = 16, 0.3
RING_J, RING_C, RING_P, RING_SIGMA, RING_RMAX, RING_WIDTH, RING_TAU, RING_VGAIN = 0.5, 2.0, 2.0, 0.5, 2.0, 1.2, 1.0, 1.0
RING_DT = 1.0
WIND_CUE, CUE_WIDTH = 6.0, 1.2
# body, agent side: controller (src/ph9.py:33, 40-41; src/ph12.py:29; src/ph11.py:127-128)
UPWIND = 180.0
CAST_PERIOD, CAST_GROW, MAXOFF = 30, 1.2, 170.0
GAIN, MAXTURN, TURN_NOISE = 0.6, 40.0, 6.0
SAT = MAXOFF/CAST_GROW
FLEE_SIDES = [90.0, 270.0]
TICK = 1                                        # one tick = one world step; not an argument


def sigmoid(z):                                 # ffcore.py:5-6
    return 1.0 / (1.0 + np.exp(-np.clip(z, -SIG_CLIP, SIG_CLIP)))


def angdiff(a, b): return (np.asarray(a) - np.asarray(b) + 180.0) % 360.0 - 180.0     # src/ph9.py:105


def cue(runs, n, deg, amp=1.0, width=1.2):      # src/ph3.py:36-41
    idx = np.arange(n)[None, :]
    c = (np.asarray(deg)/360.0*n).reshape(-1, 1)
    d = np.abs(idx - c); d = np.minimum(d, n - d)
    return amp*np.exp(-0.5*(d/width)**2)


# ------------------------------------------------------------------ core parts
class Upstream:
    """src/ph2.py:5-17 (Heeger stage)"""
    def __init__(self, runs, chans):
        n, sig = UP_N, UP_SIG
        self.n, self.sig_n, self.Rmax, self.k, self.tau = n, sig**n, UP_RMAX, UP_K, UP_TAU
        self.P = np.zeros((runs, chans))

    def step(self, x):
        u = np.maximum(x, 0.0)**self.n
        self.P += (1.0/self.tau) * (-self.P + u)
        N = self.P.shape[1]
        others = (self.P.sum(1, keepdims=True) - self.P) / max(N - 1, 1)
        return self.Rmax * self.P / (self.sig_n + self.P + self.k*others)


class Circuit:
    """src/ph2.py:19-42 with gsat None; at n 3 the noise of unit 3 on rng3 (src/ph32.py:125-142)"""
    DT, S_MAX = C_DT, C_SMAX

    def __init__(self, runs, n, rng, rng3=None):
        self.R, self.n, self.w_i, self.g, self.theta, self.k = runs, n, C_WI, C_G, C_THETA, C_K
        self.tau, self.tau_g, self.gsat, self.noise = C_TAU, C_TAUG, None, C_NOISE
        self.pool_p, self.pool_c = C_POOLP, C_POOLC
        self.rng = rng
        self.s = np.zeros((runs, n)); self.S = np.zeros((runs, 1))
        if n > 2: self.rng3 = rng3

    def memory(self): return self.s

    def step(self, y, reset=0.0):
        q = self.pool_c * np.maximum(self.s, 0.0)**self.pool_p
        pool = q.sum(1, keepdims=True) + reset
        self.S += (self.DT/self.tau_g) * (-self.S + pool)
        if self.n > 2:
            z = self.rng.standard_normal((self.R, 2))
            z = np.concatenate([z, self.rng3.standard_normal((self.R, self.n - 2))], 1)
            u = (y + self.g*sigmoid(self.k*(self.s - self.theta)) + self.w_i*q - self.w_i*self.S + self.noise*z)
        else:
            u = (y + self.g*sigmoid(self.k*(self.s - self.theta)) + self.w_i*q - self.w_i*self.S
                 + self.noise*self.rng.standard_normal(self.s.shape))
        self.s += (self.DT/self.tau) * (-self.s + np.clip(u, 0, self.S_MAX))
        return self.s


class MB:
    """src/ph4.py:18-63 with ph8.MB4's valence and step (src/ph8.py:40-99), single site (parallel False), gated"""
    def __init__(self, runs, rng):
        self.R, self.K, self.C = runs, MB_K, MB_C
        self.sparsity, self.eta_d, self.eta_p = MB_SPARSITY, MB_ETA_D, MB_ETA_P
        self.tau_code, self.tau_reinf, self.wmin, self.wmax = MB_TAU_CODE, MB_TAU_REINF, MB_WMIN, MB_WMAX
        self.beta = MB_BETA
        self.rng = rng
        self.w = np.full((runs, self.C, self.K), float(MB_W0))
        self.tc = np.zeros((runs, self.K))
        self.tr = np.zeros((runs, self.C))
        self.parallel, self.gated = False, True

    def odour(self, seed):
        r = np.random.default_rng(seed)
        m = np.zeros((self.R, self.K))
        nact = max(1, int(round(self.sparsity*self.K)))
        for i in range(self.R):
            m[i, r.choice(self.K, nact, replace=False)] = 1.0
        return m

    def out(self, code):
        return np.einsum('rck,rk->rc', self.w, code) / np.maximum(code.sum(1, keepdims=True), 1)

    def valence(self, code):
        o = self.out(code)
        return (o[:, 0] - o[:, 1]) + (o[:, 2] - o[:, 3])

    def step(self, code=None, reinf=None):
        code = np.zeros((self.R, self.K)) if code is None else code
        reinf = np.zeros((self.R, self.C)) if reinf is None else reinf
        if self.beta and code.any():
            o = self.out(code)
            drive = (o[:, 0] - o[:, 1]) + (o[:, 2] - o[:, 3])
            gate = 1.0
            if self.gated:
                gate = (reinf.sum(1, keepdims=True) <= 0.0).astype(float)
            pos = np.maximum(drive, 0.0)[:, None]
            neg = np.maximum(-drive, 0.0)[:, None]
            fb = np.zeros_like(reinf)
            fb[:, 0:1] = pos                            # H8 v2: straight back onto the original (src/ph8.py:88-90)
            fb[:, 1:2] = neg
            reinf = reinf + self.beta*fb*gate
        tc_now = np.minimum(self.tc + code, 1.0)
        tr_past = self.tr*(reinf <= 0.0)
        dw = (-self.eta_d*np.einsum('rc,rk->rck', reinf, tc_now)
              + self.eta_p*np.einsum('rc,rk->rck', tr_past, code))
        self.w = np.clip(self.w + dw, self.wmin, self.wmax)
        self.tc += (1.0/self.tau_code)*(-self.tc) + code
        self.tr += (1.0/self.tau_reinf)*(-self.tr) + reinf
        self.tc = np.minimum(self.tc, 1.0); self.tr = np.minimum(self.tr, 1.0)


# ------------------------------------------------------------------ body part (agent side)
class Ring:
    """src/ph10.py:44-78 (RingExact) at the adopted parameters"""
    DT = RING_DT

    def __init__(self, runs, rng):
        n = RING_N
        self.R, self.n, self.p, self.sigma, self.c, self.Rmax = runs, n, RING_P, RING_SIGMA, RING_C, RING_RMAX
        self.tau, self.vgain, self.noise, self.J, self.width = RING_TAU, RING_VGAIN, RING_NOISE, RING_J, RING_WIDTH
        self.rng = rng
        self.s = np.zeros((runs, n))
        i = np.arange(n)[:, None]; j = np.arange(n)[None, :]
        self.o = ((i - j + n//2) % n) - n//2
        self.ang = 2*np.pi*np.arange(n)/n

    def pos(self):
        return np.degrees(np.angle((self.s*np.exp(1j*self.ang)).sum(1))) % 360.0

    def step(self, x=None, v=0.0):
        s = self.s
        delta = np.asarray(self.vgain*v*self.n/360.0, dtype=float).reshape(-1, 1, 1)
        oo = ((self.o[None, :, :] - delta + self.n/2) % self.n) - self.n/2
        W = self.J*np.exp(-0.5*(oo/self.width)**2)
        exc = np.einsum('rij,rj->ri', W, s) + self.noise*self.rng.standard_normal(s.shape)
        if x is not None: exc = exc + x
        e = np.maximum(exc, 0.0)**self.p
        r = self.Rmax*e / (self.sigma**self.p + self.c*e.mean(1, keepdims=True))
        self.s = s + (self.DT/self.tau)*(-s + r)
        return self.s


# ------------------------------------------------------------------ the agent
def evidence_due(y, hp):
    """src/ph32.py:145-149; at two channels the same element as src/ph23.py:68-70 (design 4.3)"""
    rows = np.arange(len(hp)); committed = hp >= 0; hi = np.maximum(hp, 0)
    yo = y.copy(); yo[rows, hi] = -np.inf; other = yo.argmax(1)
    return committed & ((y[rows, other] - y[rows, hi]) > MARGIN)


class Fly:
    """Fly(runs, rng, known, nch=2, rng3=None). known: (runs, nch) values, written by the caller (supplied, or the module's
    read-out mirrored before each act). The caller learns by a.mb.step(code, reinf) after the move (U7)."""

    def __init__(self, runs, rng, known, nch=2, rng3=None):
        assert nch in (2, 3) and (nch == 2 or rng3 is not None)
        self.R, self.rng, self.known, self.nch = runs, rng, known, nch
        self.G = G_STAR
        self.up = Upstream(runs, nch)
        self.sel = Circuit(runs, nch, rng, rng3)
        self.ring = Ring(runs, rng)
        self.mb = MB(runs, rng)
        self.codes = np.stack([self.mb.odour(CODE_SEEDS[0]), self.mb.odour(CODE_SEEDS[1])], 1)
        if nch == 3: self.codes = np.concatenate([self.codes, self.mb.odour(CODE_SEEDS[2])[:, None, :]], 1)
        self.last_turn = np.zeros(runs)
        self.since = np.zeros(runs); self.silence = np.zeros(runs)
        self.flee_side = rng.choice(FLEE_SIDES, runs)                     # the only construction draw (src/ph11.py:127)
        self.cast_sign = np.ones(runs)
        self.est = np.zeros(runs)
        self.nav_hit = np.zeros(runs, bool)
        self.tgt = np.zeros(runs)
        self.due_evidence = self.due_timeout = np.zeros(runs, bool)
        self.P, self.N_hi = P_PRIOR, N_HI[nch]
        self.N = self.N_hi
        self.c = np.full((runs, nch), float(self.N_hi - self.P))
        self.present = np.ones((runs, nch), bool)
        self.sustain = np.zeros(self.R, bool); self.zreset = np.zeros(self.R, bool)
        if nch == 3:
            self.t16 = 0; self.w2 = np.full((runs, nch), NEVER); self.bb = np.full((runs, nch), NEVER)
            self.burst = np.zeros((runs, nch), bool)

    # -------------------------------------------------------------- reads
    def held(self):
        on = self.sel.memory() > HOLD
        return np.where(on.sum(1) == 1, on.argmax(1), -1)

    def chan_valence(self):
        return self.known

    def bump(self, mask):
        if mask.any():
            self.flee_side = np.where(mask, (self.flee_side + 180.0) % 360.0, self.flee_side)
            self.cast_sign = np.where(mask, -self.cast_sign, self.cast_sign)

    def estimate(self, w, wind_on):
        """body: the ring fed the rotation made, then the wind cue (src/ph13.py:56-61)"""
        self.ring.step(v=w.rot)
        if wind_on.any():
            self.ring.step(x=cue(self.R, RING_N, w.head, WIND_CUE, width=CUE_WIDTH)*wind_on[:, None])
        return self.ring.pos()

    # -------------------------------------------------------------- one tick
    def act(self, w, whiffs, wind_on):
        """ReleaseN2 (src/ph30.py:121-136) around the base act"""
        rows = np.arange(self.R); hp = self.held()
        turn, h = self._act(w, whiffs, wind_on)
        v = self.chan_valence()
        hit = (h >= 0) & whiffs[rows, np.maximum(h, 0)]
        new = (h >= 0) & (h != hp)
        negS = (hp >= 0) & (v[rows, np.maximum(hp, 0)] < 0.0)
        negZ = (h >= 0) & (v[rows, np.maximum(h, 0)] < 0.0)
        base = self.due_timeout & ~self.due_evidence & (self.sel.s > 1.0).any(1) & ~hit
        sustain = base & ~negS
        newz = new & ~negZ
        self.sustain, self.zreset = sustain, newz & ~sustain & (self.silence > 0)
        self.silence = np.where(sustain, RESET_AFTER + 1.0, np.where(newz, 0.0, self.silence))
        return turn, h

    def _act(self, w, whiffs, wind_on):
        """src/ph23.py:60-104 (nch 2) / src/ph33.py:119-177 (nch 3), measurement lines removed"""
        rows = np.arange(self.R)
        # core: stage, gain, gate
        y = self.up.step(whiffs.astype(float))*(1.0 + self.G*np.maximum(self.chan_valence(), 0.0))
        hp = self.held()
        v = self.chan_valence(); vh = v[rows, np.maximum(hp, 0)]
        y = y*~((hp >= 0)[:, None] & (v >= 0.0) & (v < vh[:, None]))
        # core: release conditions, circuit, hold
        self.due_timeout = self.silence > RESET_AFTER
        self.due_evidence = evidence_due(y, hp)
        due = self.due_timeout | self.due_evidence
        rst = np.where(due, RESET_DRIVE, 0.0)[:, None]
        self.silence = np.where(due, 0.0, self.silence)
        self.sel.step(y, reset=rst)
        h = self.held()
        # body: heading
        est = self.est = self.estimate(w, wind_on)
        # core: read-out (value of the held odour, presence, filter)
        val = np.where(h >= 0, self.known[rows, np.maximum(h, 0)], 0.0)
        hit = np.where(h >= 0, whiffs[rows, np.maximum(h, 0)], False)
        v = self.chan_valence(); vh = v[rows, np.maximum(h, 0)]
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
        held = np.zeros_like(whiffs); held[rows, np.maximum(h, 0)] = h >= 0
        self.present = (self.c < self.N) | held
        vmax = np.where(self.present, v, -np.inf).max(1)
        top = self.present & (v >= 0) & (v == vmax[:, None])
        if self.nch == 3:
            nT = top.sum(1); bT = np.where(top, self.bb, -np.inf).max(1)
            ranked = top & (self.bb == bT[:, None]) & (bT > NEVER)[:, None]
            topr = np.where((nT >= 2)[:, None], ranked, top)
            keep = (h >= 0) & (topr[rows, np.maximum(h, 0)] | (vh < 0))
            nav = np.where(keep, hit, (whiffs & topr).any(1))
        else:
            keep = (h >= 0) & ((vh == vmax) | (vh < 0))
            nav = np.where(keep, hit, (whiffs & top).any(1))
        self.nav_hit = nav
        # body: cast clock, target, flee, turn
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
