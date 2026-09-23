"""Phase 3: ring attractor (H3). Same unit nonlinearity family as the Select-and-Hold circuit,
but the units sit on a ring: neighbours excite each other and one global unit inhibits all."""
import numpy as np
from ffcore import sigmoid

class Ring:
    DT, S_MAX = 1.0, 5.0
    def __init__(self, runs, n=16, J=1.0, width=1.2, w_i=1.0, g=0.6, theta=0.5, k=8.0,
                 tau=10.0, tau_g=2.0, vgain=1.0, noise=0.01, rng=None):
        self.R, self.n, self.w_i, self.g, self.theta, self.k = runs, n, w_i, g, theta, k
        self.tau, self.tau_g, self.vgain, self.noise = tau, tau_g, vgain, noise
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self.s = np.zeros((runs, n)); self.S = np.zeros((runs, 1))
        i = np.arange(n)[:, None]; j = np.arange(n)[None, :]
        o = ((i - j + n//2) % n) - n//2                            # signed circular offset
        self.W = J*np.exp(-0.5*(o/width)**2); np.fill_diagonal(self.W, 0.0)
        self.Wp = -(o/width**2)*self.W                             # d/do of the kernel
        self.ang = 2*np.pi*np.arange(n)/n
    def pos(self):
        """population vector angle, in degrees"""
        z = (self.s*np.exp(1j*self.ang)).sum(1)
        return np.degrees(np.angle(z)) % 360.0
    def amp(self): return self.s.max(1)
    def step(self, x=None, v=0.0):
        s = self.s
        # v is angular velocity in degrees per step; delta is the kernel offset in wedges
        delta = self.vgain*v*self.n/360.0
        exc = s @ (self.W - delta*self.Wp).T                # kernel shifted by delta: moves the bump
        self.S += (self.DT/self.tau_g)*(-self.S + s.sum(1, keepdims=True))
        u = (exc + self.g*sigmoid(self.k*(s - self.theta)) - self.w_i*self.S
             + self.noise*self.rng.standard_normal(s.shape))
        if x is not None: u = u + x
        self.s = s + (self.DT/self.tau)*(-s + np.clip(u, 0, self.S_MAX))
        return self.s

def cue(runs, n, deg, amp=1.0, width=1.2):
    """landmark input: a bump of external drive centred on deg"""
    idx = np.arange(n)[None, :]
    c = (np.asarray(deg)/360.0*n).reshape(-1, 1)
    d = np.abs(idx - c); d = np.minimum(d, n - d)
    return amp*np.exp(-0.5*(d/width)**2)

def circdiff(a, b):
    return (np.asarray(a) - np.asarray(b) + 180.0) % 360.0 - 180.0

def nbumps(s, frac=0.3):
    """count contiguous groups of wedges above frac of the row max (circularly)"""
    m = s > frac*s.max(1, keepdims=True)
    out = []
    for row in m:
        if not row.any(): out.append(0); continue
        r = np.roll(row, -np.argmin(row)) if not row.all() else row
        out.append(int((np.diff(np.concatenate([[0], r.astype(int), [0]])) == 1).sum()) if not row.all() else 1)
    return np.array(out)


class RingDiv:
    """Ring attractor with divisive rather than subtractive global inhibition.
       exc_i  = sum_j Wshift[i,j] s_j + external_i
       r_i    = Rmax * relu(exc_i)^p / (sigma^p + c * mean_j relu(exc_j)^p)
       s     <- s + (1/tau) * (-s + r)
       The global unit divides instead of subtracting, which fixes total activity and leaves
       the bump position free: a continuum of stable states rather than a set of latched wedges."""
    DT = 1.0
    def __init__(self, runs, n=16, J=1.0, width=1.2, p=2.0, sigma=0.3, c=1.0, Rmax=2.0,
                 tau=10.0, vgain=1.0, noise=0.01, rng=None):
        self.R, self.n, self.p, self.sigma, self.c, self.Rmax = runs, n, p, sigma, c, Rmax
        self.tau, self.vgain, self.noise = tau, vgain, noise
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self.s = np.zeros((runs, n))
        i = np.arange(n)[:, None]; j = np.arange(n)[None, :]
        o = ((i - j + n//2) % n) - n//2
        self.W = J*np.exp(-0.5*(o/width)**2)
        self.Wp = -(o/width**2)*self.W
        self.ang = 2*np.pi*np.arange(n)/n
    def pos(self):
        return np.degrees(np.angle((self.s*np.exp(1j*self.ang)).sum(1))) % 360.0
    def amp(self): return self.s.max(1)
    def step(self, x=None, v=0.0):
        s = self.s
        delta = np.asarray(self.vgain*v*self.n/360.0, dtype=float)
        if delta.ndim: delta = delta.reshape(-1, 1)      # one angular velocity per run
        # linear in delta, so the per-run shift can be applied without building a kernel per run
        exc = s @ self.W.T - delta*(s @ self.Wp.T) + self.noise*self.rng.standard_normal(s.shape)
        if x is not None: exc = exc + x
        e = np.maximum(exc, 0.0)**self.p
        r = self.Rmax*e / (self.sigma**self.p + self.c*e.mean(1, keepdims=True))
        self.s = s + (self.DT/self.tau)*(-s + r)
        return self.s
