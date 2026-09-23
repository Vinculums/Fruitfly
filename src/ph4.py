"""Phase 4: compartment-local, timing-signed plasticity gated by reinforcement (H8 v2).

Layout, following the mushroom body as Phase 1 read it:
  - a sparse code of K units, a fraction `sparsity` active per odour;
  - C compartments, each with one output unit and one reinforcement unit;
  - weights w[c, k], one set per compartment, modified only by that compartment's own
    reinforcement unit;
  - valence = output(compartment 0) - output(compartment 1). Compartment 0 is the one whose
    reinforcement unit signals punishment and whose output unit promotes approach, so pairing
    odour with punishment depresses it and the valence falls.

Plasticity uses two eligibility traces, which is what makes the sign depend on order:
  dw = -eta_d * trace_code * reinforcement   (code first, then reinforcement -> depression)
       +eta_p * trace_reinf * code           (reinforcement first, then code -> potentiation)
"""
import numpy as np

class MB:
    def __init__(self, runs, K=500, C=2, sparsity=0.05, eta_d=0.30, eta_p=0.30,
                 tau_code=5.0, tau_reinf=5.0, w0=1.0, wmin=0.0, wmax=2.0, beta=0.0, rng=None):
        self.R, self.K, self.C = runs, K, C
        self.sparsity, self.eta_d, self.eta_p = sparsity, eta_d, eta_p
        self.tau_code, self.tau_reinf, self.wmin, self.wmax = tau_code, tau_reinf, wmin, wmax
        self.beta = beta                        # output-to-reinforcement feedback (extinction)
        self.rng = rng if rng is not None else np.random.default_rng(0)
        self.w = np.full((runs, C, K), float(w0))
        self.tc = np.zeros((runs, K))          # code eligibility trace
        self.tr = np.zeros((runs, C))          # reinforcement trace
    def odour(self, seed):
        """draw one sparse binary code per run"""
        r = np.random.default_rng(seed)
        m = np.zeros((self.R, self.K))
        nact = max(1, int(round(self.sparsity*self.K)))
        for i in range(self.R):
            m[i, r.choice(self.K, nact, replace=False)] = 1.0
        return m
    def out(self, code):
        """response of every output unit to a code, normalised by the number of active units"""
        return np.einsum('rck,rk->rc', self.w, code) / np.maximum(code.sum(1, keepdims=True), 1)
    def valence(self, code):
        o = self.out(code); return o[:, 0] - o[:, 1]
    def step(self, code=None, reinf=None):
        """one time step. code: (R,K) or None. reinf: (R,C) or None."""
        code = np.zeros((self.R, self.K)) if code is None else code
        reinf = np.zeros((self.R, self.C)) if reinf is None else reinf
        if self.beta and code.any():
            # the odour itself drives each compartment's reinforcement unit in proportion to how
            # far that compartment's output currently exceeds the other: an opponent feedback that
            # pulls an unreinforced memory back toward balance (the fly's MBON-to-DAN feedback)
            o = self.out(code); dif = o[:, 0] - o[:, 1]
            fb = np.stack([np.maximum(dif, 0.0), np.maximum(-dif, 0.0)], 1)
            reinf = reinf + self.beta*fb
        # depression: the code is already active (now or recently) when reinforcement arrives
        tc_now = np.minimum(self.tc + code, 1.0)
        # potentiation: reinforcement has ended and the code arrives afterwards. Gating by
        # (reinforcement off now) is what makes the sign depend on order rather than on overlap.
        tr_past = self.tr*(reinf <= 0.0)
        dw = (-self.eta_d*np.einsum('rc,rk->rck', reinf, tc_now)
              + self.eta_p*np.einsum('rc,rk->rck', tr_past, code))
        self.w = np.clip(self.w + dw, self.wmin, self.wmax)
        self.tc += (1.0/self.tau_code)*(-self.tc) + code
        self.tr += (1.0/self.tau_reinf)*(-self.tr) + reinf
        self.tc = np.minimum(self.tc, 1.0); self.tr = np.minimum(self.tr, 1.0)

def reinf_vec(mb, comp, amp=1.0):
    r = np.zeros((mb.R, mb.C))
    if comp is not None: r[:, comp] = amp
    return r

def pairing(mb, code, comp, order="forward", on=5, gap=5, tail=20):
    """one trial. forward: code then reinforcement. reverse: reinforcement then code.
       unpaired: code alone (comp None)."""
    cz = np.zeros_like(code)
    if order == "reverse":
        first, second = (None, comp), (code, None)
    else:
        first, second = (code, None), (None, comp)
    for _ in range(on): mb.step(code=first[0] if first[0] is not None else cz,
                                reinf=reinf_vec(mb, first[1]))
    for _ in range(gap): mb.step()
    for _ in range(on): mb.step(code=second[0] if second[0] is not None else cz,
                                reinf=reinf_vec(mb, second[1]))
    for _ in range(tail): mb.step()
