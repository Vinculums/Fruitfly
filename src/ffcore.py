"""Fruits Fly core models and task. Reimplemented from the Vinc run documents (Phase 0.1).
All simulations are vectorised over runs: state arrays have shape (runs, N)."""
import numpy as np

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60, 60)))

# ---------------------------------------------------------------- Exp1: scalar STM
class STM:
    TAU, DT = 20.0, 1.0
    def __init__(self, kind, alpha=0.0, k=8.0, theta=1.0):
        self.kind, self.alpha, self.k, self.theta, self.s = kind, alpha, k, theta, 0.0
        self.leak = 1.0 - self.DT / self.TAU
    def step(self, x):
        if self.kind == "leak": rec = 0.0
        elif self.kind == "linear": rec = self.alpha * self.s
        else: rec = self.alpha * sigmoid(self.k * (self.s - self.theta))
        self.s = self.leak * self.s + rec + x
        return self.s

def stm_run(m, amp, pulse=5, hold=400, noise=0.0, reset_at=None, seed=0):
    rng = np.random.default_rng(seed); h = []
    for t in range(pulse + hold):
        x = amp if t < pulse else 0.0
        if reset_at is not None and reset_at <= t < reset_at + 5: x = -1.0
        h.append(m.step(x + noise * rng.standard_normal()))
    return np.array(h)

# ---------------------------------------------------------------- Exp2: WTA
class WTA:
    TAU, DT, S_MAX = 10.0, 1.0, 5.0
    def __init__(self, w_i=1.0, w_e=0.5, noise=0.01, n=5, seed=0):
        self.w_i, self.w_e, self.noise = w_i, w_e, noise
        self.s = np.zeros(n); self.rng = np.random.default_rng(seed)
    def step(self, x):
        others = self.s.sum() - self.s
        u = x + self.w_e*self.s - self.w_i*others + self.noise*self.rng.standard_normal(len(self.s))
        self.s += (self.DT/self.TAU) * (-self.s + np.clip(u, 0, self.S_MAX))
        return self.s

# ---------------------------------------------------------------- Exp3/Exp4: selection + memory networks
class Net:
    """Rate network, vectorised over runs. design:
       'B'  merged, linear self-excitation w_e, all-to-all inhibition
       'B2' merged, sigmoid self-excitation g*sigmoid(k*(s-theta)), all-to-all inhibition
       'G1' B2 with one global unit (state pool S), linear self term cancels own share
       'G2' G1 + divisive input normalisation by input pool M
       'G3' G2 with S = 5*mean(s)
       'G4' G2 with S also in the divisive denominator, input gain C
       'A'  serial: WTA stage feeding 5 independent sigmoid latches"""
    DT, S_MAX = 1.0, 5.0
    def __init__(self, design, runs, n=5, w_i=1.0, g=2.0, theta=1.0, k=8.0, w_e=1.2,
                 tau=10.0, tau_g=2.0, eps=0.1, C=None, noise=0.01, rng=None):
        self.d, self.R, self.n = design, runs, n
        self.w_i, self.g, self.theta, self.k, self.w_e = w_i, g, theta, k, w_e
        self.tau, self.tau_g, self.eps, self.noise = tau, tau_g, eps, noise
        self.C = C if C is not None else eps + 1.0
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self.s = np.zeros((runs, n))
        self.S = np.zeros((runs, 1)); self.M = np.zeros((runs, 1))
        if design == "A":
            self.w = np.zeros((runs, n))          # WTA stage; self.s is the latch bank
    def memory(self): return self.s
    def step(self, x, reset=0.0):
        """x: (runs, n) external input. reset: scalar reset drive (design specific path)."""
        d = self.d; xi = self.noise * self.rng.standard_normal(self.s.shape)
        if d == "A":
            others = self.w.sum(1, keepdims=True) - self.w
            u = x + 0.5*self.w - 1.0*others + xi
            self.w += (self.DT/10.0) * (-self.w + np.clip(u, 0, self.S_MAX))
            drive = 0.2*np.maximum(self.w - 1.5, 0.0)
            self.s = 0.95*self.s + 0.10*sigmoid(8.0*(self.s - 1.0)) + drive - reset
            return self.s
        if d in ("B", "B2"):
            others = self.s.sum(1, keepdims=True) - self.s
            selfx = self.w_e*self.s if d == "B" else self.g*sigmoid(self.k*(self.s - self.theta))
            u = x + selfx - self.w_i*others + xi - reset
        else:
            pool = self.s.sum(1, keepdims=True) if d != "G3" else 5.0*self.s.mean(1, keepdims=True)
            self.S += (self.DT/self.tau_g) * (-self.S + pool + reset)
            if d != "G1":
                self.M += (self.DT/self.tau_g) * (-self.M + x.mean(1, keepdims=True))
                den = self.eps + np.maximum(self.M, 0.0) + (self.S if d == "G4" else 0.0)
                x = x * self.C / den
            own = 5.0/self.n if d == "G3" else 1.0   # each unit cancels exactly its own share of the pool
            u = x + self.g*sigmoid(self.k*(self.s - self.theta)) + self.w_i*own*self.s - self.w_i*self.S + xi
        self.s += (self.DT/self.tau) * (-self.s + np.clip(u, 0, self.S_MAX))
        return self.s

RESET_AMP = {"A": 1.0, "B": 10.0, "B2": 10.0, "G1": 10.0, "G2": 10.0, "G3": 10.0, "G4": 10.0}

def trial(net, target, d=0.4, cue=100, delay=300, x0=1.0, noise_sd=0.3, distractor=None,
          reset=False, dist_at=100, dist_len=20, scaled=False):
    """One cued delayed-choice trial on every run. target: (runs,) int. Returns outcome codes:
       1 correct, 0 wrong, -1 abstain (none held), -2 several held."""
    R, n = net.R, net.n; rows = np.arange(R)
    if reset:
        for _ in range(30): net.step(np.zeros((R, n)), reset=RESET_AMP[net.d])
    for _ in range(cue):
        k = float(x0) if scaled else 1.0      # scaled=True: difference and noise scale with x0 (Exp4)
        x = np.full((R, n), float(x0)); x[rows, target] += d*k
        x += noise_sd*k*net.rng.standard_normal((R, n))
        net.step(x)
    for t in range(delay):
        x = np.zeros((R, n))
        if distractor is not None and dist_at <= t < dist_at + dist_len:
            x[rows, (target + 1) % n] = distractor
        net.step(x)
    held = net.memory() > 1.0; cnt = held.sum(1)
    out = np.full(R, -1); out[cnt > 1] = -2
    one = cnt == 1; out[one] = (held[one].argmax(1) == target[one]).astype(int)
    return out

def cwa(out):
    """correct / wrong / abstain counts (several-held counted as wrong)."""
    return int((out == 1).sum()), int(((out == 0) | (out == -2)).sum()), int((out == -1).sum())
