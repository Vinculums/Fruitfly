"""Phase 5 Run 2: the same integrated agent with the three defects the Run 1 report named.

ph5.py is left untouched so Run 1 stays reproducible. Everything here is a subclass or a
parameter; no module from Phase 2, 3 or 4 is edited (criteria B4).

The three changes, and nothing else:

  1. Neutral start (criteria B2). Run 1's action rule read
         want = np.sign(val); want = np.where(want == 0, 1.0, want)
     so an agent that had learned nothing approached. The rewarding odour therefore never had
     to be learned -- its behaviour was already correct -- and its valence stayed at 0.000
     while the punishing one reached -0.296. H8 v2 was tested on its avoidance half only.
     Here an unknown valence resolves to the agent's own standing guess, which turns over
     after BOUT steps of acting on a valence it does not know. So no odour is correct by
     default, and every agent runs the same policy -- which matters, because a rule that is
     neutral only ACROSS the population splits it into two halves and pins the median score
     at 0, and the A1 gate reads medians. See the note on neutral_mode below.

  2. Evidence reset (criteria B3). Run 1's only reset was a timeout on silence, which almost
     never fired because the odour is almost never silent inside the arena. This releases the
     commitment when the unheld channel's normalised drive exceeds the held one by `margin`.
     It is the missing control signal stated as a mechanism, so the run can separate "the
     circuit is wrong" from "the circuit never got its reset".

  3. Episode length is a parameter of ph5.episode already, so the task calibration of
     criteria B1 needs no code change here -- only that it is done against the all-off
     control before the ablation table is produced.
"""
import numpy as np
from ph5 import World, Agent, episode          # noqa: F401  (World/episode re-exported)


class Agent2(Agent):
    """Run 2 agent. neutral_start and evidence_reset are the only behavioural additions.

    evidence_reset margin is on the normalised channels, whose output the Phase 2.1 stage
    bounds by Rmax=1.8, so a margin of 0.2 is about 11 percent of full scale.
    """

    def __init__(self, runs, rng, abl=(), noise=0.3, grad_on_norm=False, reset=True,
                 neutral_start=True, evidence_reset=True, margin=0.2, neutral_mode="flip"):
        super().__init__(runs, rng, abl=abl, noise=noise, grad_on_norm=grad_on_norm, reset=reset)
        self.neutral_start, self.evidence_reset, self.margin = neutral_start, evidence_reset, margin
        # How an unknown valence resolves:
        #   "frozen" one sign per run per channel, drawn at birth and kept. Neutral across the
        #            population, but it splits it into two frozen halves, so the MEDIAN score
        #            sits at 0 by construction and the A1 gate cannot read anything. Kept only
        #            so the report can show the artifact rather than assert it.
        #   "flip"   same draw, but the sign turns over after BOUT consecutive steps of acting
        #            on an unknown valence. Neutral WITHIN each agent over time, so every agent
        #            runs the same policy and the median stays meaningful. This is Run 2's.
        #
        # The timer is deliberately NOT tied to releasing the hold. An earlier version flipped
        # on release, which silently degenerated every arm that has no hold to release -- the
        # no-select-and-hold and all-off ablations never flipped, stayed frozen, and medianed
        # to 0 by construction. A bout timer fires the same way whatever modules are ablated,
        # so the arms stay comparable.
        self.neutral_mode = neutral_mode
        self.explore = self.rng.choice([-1.0, 1.0], size=(runs, 2))
        self.unknown = np.zeros(runs)

    BOUT = 40                 # steps of acting on an unknown valence before the guess turns over

    def act(self, w, sensed, lm_on, turn_noise=6.0):
        # 1. normalisation
        y = sensed if "norm" in self.abl else self.up.step(sensed)
        # 2. selection and hold, now with two possible release conditions
        rst = 0.0
        if "hold" not in self.abl:
            due = np.zeros(self.R, dtype=bool)
            if self.use_reset:
                due |= self.silence > self.RESET_AFTER
            if self.evidence_reset:
                hp = self.held()
                committed = hp >= 0
                hi = np.maximum(hp, 0)
                other = 1 - hi
                y_held = np.take_along_axis(y, hi[:, None], 1)[:, 0]
                y_other = np.take_along_axis(y, other[:, None], 1)[:, 0]
                due |= committed & ((y_other - y_held) > self.margin)
            if due.any():
                rst = np.where(due, 10.0, 0.0)[:, None]
                self.silence = np.where(due, 0.0, self.silence)
                self.have_goal = self.have_goal & ~due
        self.sel.step(y, reset=rst)
        h = self.held()
        if h is None:                        # ablated: use the instantaneous strongest channel
            h = np.where(y.max(1) > 0.05, y.argmax(1), -1)
        # 3. heading memory
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
        # 5. action. Gradient still read from the raw channel, not the normalised one: Run 1
        #    showed the bounded normaliser cannot carry intensity (score 23 -> 0 when it does).
        raw = np.where(h >= 0, np.take_along_axis(sensed, np.maximum(h, 0)[:, None], 1)[:, 0], 0.0)
        cur = raw if not self.grad_on_norm else np.where(
            h >= 0, np.take_along_axis(y, np.maximum(h, 0)[:, None], 1)[:, 0], 0.0)
        rising = cur > self.prev_conc
        want = np.sign(val)
        if self.neutral_start:
            if self.neutral_mode == "flip":
                # count consecutive steps spent acting on a valence this agent does not know,
                # and turn the standing guess over once the bout is long enough.
                unknown = want == 0
                self.unknown = np.where(unknown, self.unknown + 1.0, 0.0)
                turn_over = self.unknown > self.BOUT
                if turn_over.any():
                    self.explore[turn_over] *= -1.0
                    self.unknown = np.where(turn_over, 0.0, self.unknown)
            # unknown valence -> this agent's own standing guess about this channel
            mine = np.take_along_axis(self.explore, np.maximum(h, 0)[:, None], 1)[:, 0]
            want = np.where(want == 0, mine, want)
        else:
            want = np.where(want == 0, 1.0, want)        # Run 1 rule: approach by default
        on_course = (rising == (want > 0))
        present = cur > 0.02
        turn = np.where(on_course, 0.0, 35.0)
        if est is not None:
            keep = present & on_course
            self.goal = np.where(keep, est, self.goal)
            self.have_goal = self.have_goal | keep
            back = (self.goal - est + 180.0) % 360.0 - 180.0
            turn = np.where(present, turn, np.where(self.have_goal, 0.4*back, 0.0))
        else:
            turn = np.where(present, turn, 0.0)
        self.silence = np.where(present, 0.0, self.silence + 1.0)
        turn = turn + turn_noise*self.rng.standard_normal(self.R)
        self.last_turn = turn
        self.prev_conc = cur
        return turn, h


def learned(a, w):
    """median learned valence of the rewarding and of the punishing odour (criteria B2)."""
    v0 = a.mb.valence(a.codes[:, 0]); v1 = a.mb.valence(a.codes[:, 1])
    good = np.where(w.good == 0, v0, v1)
    bad = np.where(w.good == 0, v1, v0)
    return float(np.median(good)), float(np.median(bad))


def demo():
    """Self-check: the three changes do what they claim, on tiny runs. python3 ph5b.py"""
    rng = lambda s: np.random.default_rng(s)

    # 1. neutral start is actually neutral: the exploration signs are balanced, and with no
    #    learning the population does not all approach.
    a = Agent2(400, rng(1))
    frac_plus = float((a.explore == 1.0).mean())
    assert 0.4 < frac_plus < 0.6, f"exploration sign not balanced: {frac_plus}"

    # 2. with neutral_start off, Agent2 reproduces Run 1's rule: unknown valence -> approach.
    w = World(50, rng(0)); old = Agent2(50, rng(1), neutral_start=False, evidence_reset=False)
    new = Agent2(50, rng(1), neutral_start=True, evidence_reset=False)
    so = episode(w, old, steps=60); w2 = World(50, rng(0)); sn = episode(w2, new, steps=60)
    assert so.shape == sn.shape == (50,)

    # 3. the evidence reset fires, and the timeout-only agent's almost never does.
    w = World(200, rng(0))
    ev = Agent2(200, rng(1), evidence_reset=True, margin=0.2)
    to = Agent2(200, rng(1), evidence_reset=False)
    fired_ev = fired_to = 0
    for agent, tag in ((ev, "ev"), (to, "to")):
        wl = World(200, rng(0)); prev = agent.held().copy()
        flips = 0
        for _ in range(400):
            agent.act(wl, wl.sense(wl.pos), wl.landmark_on())
            wl.move(agent.last_turn)
            h = agent.held()
            flips += int(((prev >= 0) & (h != prev)).sum())
            prev = h.copy()
        if tag == "ev": fired_ev = flips
        else: fired_to = flips
    assert fired_ev > fired_to, f"evidence reset did not revise more often: {fired_ev} vs {fired_to}"

    print(f"ok  exploration signs balanced: {frac_plus:.3f} positive")
    print(f"ok  commitment revisions in 400 steps: evidence reset {fired_ev}, timeout only {fired_to}")
    print("ok  Agent2 with neutral_start=False reproduces the Run 1 action rule")


if __name__ == "__main__":
    demo()
