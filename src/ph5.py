"""Phase 5: integrated agent. Wires together the pieces adopted in Phases 2 to 4.

World: a square arena with two odour sources. Each source emits its own odour channel with a
Gaussian concentration profile, and the plume is intermittent: on any step the whole odour
signal may be absent. A distal landmark gives an absolute heading reference, also intermittent.
One source is rewarding and one punishing; which is which is not innate and must be learned by
arriving at them.

Agent, in order:
  1. upstream normalisation (Phase 2.1)          -> bounded, scale-invariant odour channels
  2. Select-and-Hold (Phase 0.2 spec, G1 core)   -> commits to one odour and holds it through gaps
  3. ring attractor (Phase 3, design D3)         -> heading, updated by own turning, reset by landmark
  4. gated plasticity (Phase 4, H8 v2)           -> valence of the held odour
  5. action: steer by the gradient of the held odour while it is present; when it is absent, hold
     the course the heading memory says was working. Sign of the turn is set by the valence.
"""
import numpy as np
from ph2 import Upstream, Circuit
from ph3 import RingDiv
from ph4 import MB

ARENA, SRC_SIGMA, HIT_R = 40.0, 9.0, 4.0

class World:
    def __init__(self, runs, rng, p_odour=1.0, p_landmark=0.3):
        self.R, self.rng = runs, rng
        self.p_odour, self.p_landmark = p_odour, p_landmark
        self.src = rng.uniform(6.0, ARENA - 6.0, (runs, 2, 2))     # two sources, x and y
        self.good = rng.integers(0, 2, runs)                        # which one is rewarding
        self.pos = rng.uniform(0, ARENA, (runs, 2))
        self.head = rng.uniform(0, 360, runs)
    def conc(self, pos):
        d = np.linalg.norm(pos[:, None, :] - self.src, axis=2)
        return np.exp(-0.5*(d/SRC_SIGMA)**2)                        # (R,2)
    def sense(self, pos):
        c = self.conc(pos)
        on = self.rng.random(self.R) < self.p_odour
        return c*on[:, None]
    def landmark_on(self):
        return self.rng.random(self.R) < self.p_landmark
    def move(self, turn, speed=0.6):
        self.head = (self.head + turn) % 360.0
        a = np.radians(self.head)
        step = speed*np.stack([np.cos(a), np.sin(a)], 1)
        p = self.pos + step
        # reflect off the walls rather than clipping, so an agent cannot get stuck against one
        for k, flip in ((0, 180.0), (1, 0.0)):
            out = (p[:, k] < 0) | (p[:, k] > ARENA)
            if out.any():
                p[out, k] = np.clip(2*np.clip(p[out, k], 0.0, ARENA) - p[out, k], 0.0, ARENA)
                self.head[out] = (flip - self.head[out]) % 360.0
        self.pos = p
    def at_source(self):
        d = np.linalg.norm(self.pos[:, None, :] - self.src, axis=2)
        return d < HIT_R                                            # (R,2) bool

class Agent:
    """abl: any of 'norm', 'hold', 'head', 'learn', or 'all'."""
    RESET_AFTER = 40          # steps of silence on the held channel before the hold is cleared

    def __init__(self, runs, rng, abl=(), noise=0.3, grad_on_norm=False, reset=True):
        self.R, self.rng, self.abl, self.grad_on_norm = runs, rng, set(abl), grad_on_norm
        if "all" in self.abl: self.abl = {"norm", "hold", "head", "learn"}
        self.up = Upstream(n=1.5, sig=0.05, Rmax=1.8, k=0.8, runs=runs, chans=2)
        self.sel = Circuit(runs, n=2, theta=1.0, k=12.0, noise=0.01, rng=rng)
        self.ring = RingDiv(runs, n=16, J=0.5, c=2.0, p=2.0, sigma=0.3, Rmax=2.0,
                            width=1.2, vgain=10.0, noise=noise, rng=rng)
        self.mb = MB(runs, K=200, C=2, sparsity=0.05, eta_d=0.10, eta_p=0.30, beta=0.15, rng=rng)
        self.codes = np.stack([self.mb.odour(101), self.mb.odour(102)], 1)   # (R,2,K)
        self.last_turn = np.zeros(runs)
        self.prev_conc = np.zeros(runs)
        self.goal = np.zeros(runs); self.have_goal = np.zeros(runs, bool)
        self.silence = np.zeros(runs); self.use_reset = reset
    def held(self):
        """index of the odour the Select-and-Hold circuit is committed to, or -1"""
        if "hold" in self.abl: return None
        s = self.sel.memory(); on = s > 1.0
        idx = np.where(on.sum(1) == 1, on.argmax(1), -1)
        return idx
    def act(self, w, sensed, lm_on, turn_noise=6.0):
        # 1. normalisation
        y = sensed if "norm" in self.abl else self.up.step(sensed)
        # 2. selection and hold. Without a reset the circuit commits once, on whatever weak
        #    far-field evidence arrives first, and never revises it. The reset here is a timeout
        #    on silence: the control signal Exp3 flagged and Phase 1 found no anchor for.
        rst = 0.0
        if self.use_reset and "hold" not in self.abl:
            due = self.silence > self.RESET_AFTER
            if due.any():
                rst = np.where(due, 10.0, 0.0)[:, None]
                self.silence = np.where(due, 0.0, self.silence)
                self.have_goal = self.have_goal & ~due
        self.sel.step(y, reset=rst)
        h = self.held()
        if h is None:                        # ablated: use the instantaneous strongest channel
            h = np.where(y.max(1) > 0.05, y.argmax(1), -1)
        # 3. heading memory. The ring is the agent's own estimate of where it is pointing:
        #    integrated from its own commanded turns and pulled back by the landmark when visible.
        if "head" not in self.abl:
            from ph3 import cue
            self.ring.step(v=self.last_turn)
            if lm_on.any():
                c = cue(self.R, 16, w.head, 1.5, width=1.2)*lm_on[:, None]
                self.ring.step(x=c)
            est = self.ring.pos()
        else:
            est = None
        # 4. valence of the held odour
        val = np.zeros(self.R)
        if "learn" not in self.abl:
            for k in (0, 1):
                m = h == k
                if m.any(): val[m] = self.mb.valence(self.codes[:, k])[m]
        # 5. action
        # The gradient is read from the raw concentration of the selected channel, not from the
        # normalised one. The normaliser bounds its output (Phase 2.1), which is what makes it
        # scale-invariant and distractor-proof and also what destroys the intensity the steering
        # rule needs. Normalisation decides identity; the raw signal carries the gradient.
        raw = np.where(h >= 0, np.take_along_axis(sensed, np.maximum(h, 0)[:, None], 1)[:, 0], 0.0)
        cur = raw if not self.grad_on_norm else np.where(
            h >= 0, np.take_along_axis(y, np.maximum(h, 0)[:, None], 1)[:, 0], 0.0)
        rising = cur > self.prev_conc
        want = np.sign(val); want = np.where(want == 0, 1.0, want)   # unknown valence: sample it
        on_course = (rising == (want > 0))
        present = cur > 0.02
        turn = np.where(on_course, 0.0, 35.0)
        if est is not None:
            # remember the course that was working, in the agent's own heading frame
            keep = present & on_course
            self.goal = np.where(keep, est, self.goal)
            self.have_goal = self.have_goal | keep
            back = (self.goal - est + 180.0) % 360.0 - 180.0
            turn = np.where(present, turn, np.where(self.have_goal, 0.4*back, 0.0))
        else:
            turn = np.where(present, turn, 0.0)      # no heading estimate: just keep going
        self.silence = np.where(present, 0.0, self.silence + 1.0)
        turn = turn + turn_noise*self.rng.standard_normal(self.R)
        self.last_turn = turn
        self.prev_conc = cur
        return turn, h

def episode(w, a, steps=400, train=True):
    score = np.zeros(a.R)
    for t in range(steps):
        sensed = w.sense(w.pos)
        turn, h = a.act(w, sensed, w.landmark_on())
        w.move(turn)
        hit = w.at_source()
        for k in (0, 1):
            arrived = hit[:, k]
            if not arrived.any(): continue
            rewarding = (w.good == k)
            score += arrived*np.where(rewarding, 1.0, -1.0)
            if train and "learn" not in a.abl:
                # reinforcement: compartment 0 punishment, compartment 1 reward
                comp = np.where(rewarding, 1, 0)
                code = a.codes[:, k]*arrived[:, None]
                rv = np.zeros((a.R, 2)); rv[np.arange(a.R), comp] = arrived*1.0
                # The agent is inside the odour while it is being reinforced, so code and
                # reinforcement are simultaneous. Presenting them on alternate steps instead
                # turns every repetition after the first into a reverse pairing, and the
                # potentiation term then inverts the sign of what is learned.
                a.mb.step(code=code, reinf=rv)
    return score
