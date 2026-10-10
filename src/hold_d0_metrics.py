"""D0 arithmetic on fixed paths; no random generator or agent mutation."""
import numpy as np


def plume_probability(world, source):
    """World2.sense probability at the PRE-move sensing position, no draw."""
    rows = np.arange(world.R)
    src = world.src[rows, source]
    along = world.pos[:, 0] - src[:, 0]
    cross = np.abs(world.pos[:, 1] - src[:, 1])
    # The inherited World2 law; values imported from the same world modules.
    import ph11
    cone = (along > 0) & (along < ph11.LMAX) & (cross < ph11.W0 + ph11.SLOPE * along)
    near = np.linalg.norm(world.pos - src, axis=1) < 3.0
    return (cone | near) * world.p_hit * np.exp(-np.maximum(along, 0.0) / ph11.LAM)


def burst_model():
    """46 post-tick states: the two most recent whiffs in the last nine ticks.

    Age zero is the current tick; older whiffs cannot affect a future burst.
    A burst needs the current whiff and two preceding whiffs within nine ticks.
    """
    states = [()] + [(a,) for a in range(9)] + [(a, b) for a in range(9) for b in range(a + 1, 9)]
    index = {s: i for i, s in enumerate(states)}
    quiet, hit, burst = [], [], []
    for state in states:
        aged = tuple(x + 1 for x in state)
        quiet.append(index[tuple(x for x in aged if x < 9)])
        hit.append(index[tuple(x for x in ((0,) + aged)[:2] if x < 9)])
        burst.append(len(state) == 2)
    return np.array(quiet), np.array(hit), np.array(burst)


def exact_proxy(p_b, p_d):
    """Exact time-varying Bernoulli expectations conditional on supplied paths.

    Independent B/D draws. The joint tied-state distribution carries equality
    of their MOST RECENT burst timestamps, excluding the never/never state.
    Whiff-history marginals exactly implement the Poisson-binomial nine-tick
    window. No stationary approximation or random draw is used.
    Tied-single events exclude a burst of the whiffing channel. Neither agent
    identity nor presence is modelled; these counts are exposure upper bounds.
    """
    p_b, p_d = np.asarray(p_b), np.asarray(p_d)
    if p_b.shape != p_d.shape or p_b.ndim != 2:
        raise ValueError('probabilities must have identical (steps, rows) shape')
    if not (np.isfinite(p_b).all() and np.isfinite(p_d).all() and
            ((p_b >= 0) & (p_b <= 1)).all() and ((p_d >= 0) & (p_d <= 1)).all()):
        raise ValueError('invalid probability')
    steps, rows = p_b.shape
    quiet, hit, burst = burst_model()
    n = len(quiet)
    marginal_b = np.zeros((rows, n)); marginal_b[:, 0] = 1
    marginal_d = marginal_b.copy()
    tied = np.zeros((rows, n, n))
    offsets = np.arange(rows)[:, None] * n
    def move_marginal(mass, destination):
        return np.bincount((offsets + destination).ravel(), weights=mass.ravel(), minlength=rows*n).reshape(rows, n)
    joint_offsets = np.arange(rows)[:, None, None] * n*n
    left_index = np.arange(n)[None, :, None]
    right_index = np.arange(n)[None, None, :]
    def move_axis(mass, destination, axis):
        dest = joint_offsets + (destination[None, :, None]*n + right_index if axis == 1 else left_index*n + destination[None, None, :])
        return np.bincount(dest.ravel(), weights=mass.ravel(), minlength=rows*n*n).reshape(rows, n, n)
    simultaneous = np.zeros(rows); occupancy = np.zeros(rows); single = np.zeros(rows)
    for t in range(steps):
        b, d = p_b[t, :, None], p_d[t, :, None]
        burst_b = move_marginal(marginal_b * burst * b, hit)
        burst_d = move_marginal(marginal_d * burst * d, hit)
        simultaneous += burst_b.sum(1) * burst_d.sum(1)
        # A tie survives this tick only when neither channel bursts, or both
        # burst together (the latter resets equality to the current timestamp).
        non_b, non_d = ~burst, ~burst
        single += (tied * (b[:, :, None]*(1-d[:, None, :])*non_b[None, :, None] +
                           (1-b[:, :, None])*d[:, None, :]*non_d[None, None, :])).sum((1, 2))
        left = move_axis(tied * (1-b[:, :, None]), quiet, 1)
        left += move_axis(tied * b[:, :, None] * non_b[None, :, None], hit, 1)
        tied = move_axis(left * (1-d[:, None, :]), quiet, 2)
        tied += move_axis(left * d[:, None, :] * non_d[None, None, :], hit, 2)
        tied += burst_b[:, :, None] * burst_d[:, None, :]
        occupancy += tied.sum((1, 2))
        marginal_b = move_marginal(marginal_b*(1-b), quiet) + move_marginal(marginal_b*b, hit)
        marginal_d = move_marginal(marginal_d*(1-d), quiet) + move_marginal(marginal_d*d, hit)
    def expected(values):
        return dict(expected_total=float(values.sum()), expected_per_row=values.tolist())
    return dict(simultaneous_bursts=expected(simultaneous), latest_burst_tie_row_steps=expected(occupancy),
                tied_single_nonburst_row_steps=expected(single),
                expected_exposed_rows_upper_bound=float(np.minimum(single, 1).sum()),
                probability_at_least_40_rows_upper_bound=float(min(np.minimum(single, 1).sum()/40, 1)),
                interpretation='exact expectations conditional on W1D sensing paths; no presence, identity, command or benefit prediction')


def hold_records(np, samples, initial):
    """One record per contiguous held identity, including initial/censored holds.

    Release conditions are reset requests, not immediate circuit releases.
    Consecutive resets are recorded separately; lag is from first request to
    identity exit, with right censoring represented explicitly.
    """
    rows = len(initial['h']); active = [None] * rows; records = []
    def start(row, h, step, counter, inherited=False):
        return dict(row=row, channel=int(h), formation_step=step, inherited_at_start=inherited,
                    formation_counter=float(counter), maximum_held_counter=float(counter),
                    timeout_reset_steps=0, evidence_reset_steps=0, both_reset_steps=0,
                    first_reset_step=None, first_reset_cause=None, max_consecutive_reset_steps=0,
                    last_reset_step=None, last_reset_cause=None,
                    current_consecutive_reset_steps=0, survived_evidence_reset_steps=0,
                    maximum_counter_surviving_evidence_reset=None)
    for row, h in enumerate(initial['h']):
        if h >= 0: active[row] = start(row, h, -1, initial['c'][row, h], True)
    for t, s in enumerate(samples):
        for row in range(rows):
            record = active[row]
            if record is not None:
                old = record['channel']
                to, ev = bool(s['timeout'][row]), bool(s['evidence'][row])
                due = to or ev
                record['timeout_reset_steps'] += int(to)
                record['evidence_reset_steps'] += int(ev)
                record['both_reset_steps'] += int(to and ev)
                streak = record['current_consecutive_reset_steps'] + 1 if due else 0
                record['current_consecutive_reset_steps'] = streak
                record['max_consecutive_reset_steps'] = max(record['max_consecutive_reset_steps'], streak)
                if due and record['first_reset_step'] is None:
                    record['first_reset_step'] = t
                    record['first_reset_cause'] = 'both' if to and ev else 'timeout' if to else 'evidence'
                if due:
                    record['last_reset_step'] = t
                    record['last_reset_cause'] = 'both' if to and ev else 'timeout' if to else 'evidence'
                # Count only post-circuit states that still hold this identity.
                if s['h'][row] == old:
                    record['maximum_held_counter'] = max(record['maximum_held_counter'], float(s['c'][row, old]))
                    record['survived_evidence_reset_steps'] += int(ev)
                    if ev:
                        previous = record['maximum_counter_surviving_evidence_reset']
                        record['maximum_counter_surviving_evidence_reset'] = max(
                            0 if previous is None else previous, float(s['c'][row, old]))
                else:
                    record.update(exit_step=t, right_censored=False,
                                  exit_reset_cause='both' if to and ev else 'timeout' if to else 'evidence' if ev else 'no_reset_on_exit',
                                  reset_to_exit_lag=None if record['first_reset_step'] is None else t-record['first_reset_step'],
                                  last_reset_to_exit_lag=None if record['last_reset_step'] is None else t-record['last_reset_step'],
                                  final_consecutive_reset_steps=streak,
                                  last_whiff_to_exit_lag=float(s['c'][row, old]))
                    record.pop('current_consecutive_reset_steps')
                    records.append(record); active[row] = None
            h = s['h'][row]
            if h >= 0 and active[row] is None:
                active[row] = start(row, h, t, s['c'][row, h])
    for record in active:
        if record is not None:
            record.update(exit_step=None, right_censored=True, exit_reset_cause=None,
                          reset_to_exit_lag=None, last_reset_to_exit_lag=None,
                          final_consecutive_reset_steps=record.pop('current_consecutive_reset_steps'),
                          last_whiff_to_exit_lag=None)
            records.append(record)
    return records
