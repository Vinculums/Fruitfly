"""Phase 2 designs: upstream normalisation stage (H6) and option-count calibration (H7)."""
import numpy as np
from ffcore import sigmoid

class Upstream:
    """Separate sensory stage. Reads external input only; never reads the memory state.
       y_i = Rmax * u_i / (sig^n + u_i + k*mean_{j!=i} u_j),  u = x^n  (Heeger/Olsen form,
       own term in the denominator => output bounded by Rmax whatever the input)."""
    def __init__(self, n=1.5, sig=0.05, Rmax=1.8, k=0.8, tau=2.0, runs=1, chans=5):
        self.n, self.sig_n, self.Rmax, self.k, self.tau = n, sig**n, Rmax, k, tau
        self.P = np.zeros((runs, chans))          # low-passed u, the pooled sensory drive
    def step(self, x):
        u = np.maximum(x, 0.0)**self.n
        self.P += (1.0/self.tau) * (-self.P + u)
        N = self.P.shape[1]
        others = (self.P.sum(1, keepdims=True) - self.P) / max(N - 1, 1)
        return self.Rmax * self.P / (self.sig_n + self.P + self.k*others)

class Circuit:
    """G1 core from the architecture spec, with an optional saturating global unit (H7).
       gsat None -> pool passed through linearly (exactly G1). gsat (Smax, kappa) -> the
       global unit saturates, so pooled inhibition stops growing with the option count."""
    DT, S_MAX = 1.0, 5.0
    def __init__(self, runs, n=5, w_i=1.0, g=2.0, theta=1.0, k=8.0, tau=10.0, tau_g=2.0,
                 gsat=None, pool_p=1.0, pool_c=1.0, noise=0.01, rng=None):
        self.R, self.n, self.w_i, self.g, self.theta, self.k = runs, n, w_i, g, theta, k
        self.tau, self.tau_g, self.gsat, self.noise = tau, tau_g, gsat, noise
        self.pool_p, self.pool_c = pool_p, pool_c
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self.s = np.zeros((runs, n)); self.S = np.zeros((runs, 1))
    def memory(self): return self.s
    def step(self, y, reset=0.0):
        q = self.pool_c * np.maximum(self.s, 0.0)**self.pool_p   # supralinear pool when p>1
        pool = q.sum(1, keepdims=True) + reset
        if self.gsat is not None:
            Smax, kappa = self.gsat
            pool = Smax * pool / (kappa + pool)
        self.S += (self.DT/self.tau_g) * (-self.S + pool)
        u = (y + self.g*sigmoid(self.k*(self.s - self.theta)) + self.w_i*q - self.w_i*self.S
             + self.noise*self.rng.standard_normal(self.s.shape))
        self.s += (self.DT/self.tau) * (-self.s + np.clip(u, 0, self.S_MAX))
        return self.s

class Agent:
    """Upstream stage feeding the circuit. up=None -> no normalisation (control)."""
    def __init__(self, runs, n=5, up=None, **ckw):
        self.R, self.n = runs, n
        self.c = Circuit(runs, n=n, **ckw)
        self.up = Upstream(runs=runs, chans=n, **up) if up is not None else None
    def step(self, x, reset=0.0):
        y = self.up.step(x) if self.up is not None else x
        return self.c.step(y, reset=reset)
    def memory(self): return self.c.memory()

def trial(a, target, d=0.4, cue=100, delay=300, x0=1.0, noise_sd=0.3, distractor=None,
          reset=False, dist_at=100, dist_len=20, scaled=True, rng=None):
    R, n = a.R, a.n; rows = np.arange(R); rng = rng or np.random.default_rng(7)
    if reset:
        for _ in range(30): a.step(np.zeros((R, n)), reset=10.0)
    kk = float(x0) if scaled else 1.0
    for _ in range(cue):
        x = np.full((R, n), float(x0)); x[rows, target] += d*kk
        x += noise_sd*kk*rng.standard_normal((R, n))
        a.step(x)
    for t in range(delay):
        x = np.zeros((R, n))
        if distractor is not None and dist_at <= t < dist_at + dist_len:
            x[rows, (target + 1) % n] = distractor
        a.step(x)
    held = a.memory() > 1.0; cnt = held.sum(1)
    out = np.full(R, -1); out[cnt > 1] = 0
    one = cnt == 1; out[one] = (held[one].argmax(1) == target[one]).astype(int)
    return out

def cwa(o): return int((o==1).sum()), int((o==0).sum()), int((o==-1).sum())
