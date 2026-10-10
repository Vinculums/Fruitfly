"""Register the owner-approved hold designs after a read-only seed scan."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = {"bench": [86240001, 86240002], "dev": [86240101, 86240102],
         "eval": [86240201, 86240202], "bootstrap": 86240301}


def seed_numbers():
    worlds = [SEEDS[k][0] for k in ("bench", "dev", "eval")]
    agents = [SEEDS[k][1] for k in ("bench", "dev", "eval")]
    return sorted(set(worlds + agents + [SEEDS["bootstrap"]]
                      + [s + d for s in worlds for d in (10000, 30000)]
                      + [s + d for s in agents for d in (20000, 30000)]))


def scan():
    pattern = re.compile(rb"(?<!\d)(?:" + b"|".join(str(s).encode() for s in seed_numbers()) + rb")(?!\d)")
    hits, files = [], 0
    for p in ROOT.rglob("*"):
        if not p.is_file() or any(x in (".git", "__pycache__") for x in p.relative_to(ROOT).parts):
            continue
        if p == Path(__file__).resolve():
            continue  # candidate declaration only; no experiment has run
        files += 1
        with p.open("rb") as f:
            tail = b""
            while block := f.read(4 * 1024 * 1024):
                buf = tail + block
                matches = [m.group().decode() for m in pattern.finditer(buf)]
                if matches:
                    hits.append({"path": p.relative_to(ROOT).as_posix(), "seeds": sorted(set(matches))})
                    break
                tail = buf[-32:]
    return {"files": files, "numbers": seed_numbers(), "hits": hits,
            "exclusions": [".git", "__pycache__", "tools/prepare_hold_final.py (candidate declaration)"],
            "derived_streams": "world + balance; world + D_OFF; agent + cast; agent + A3_OFF"}


def main():
    audit = scan()
    if audit["hits"]:
        raise RuntimeError(json.dumps(audit["hits"]))
    config = ROOT / "config/hold-stage2-seeds.json"
    config.write_text(json.dumps(SEEDS, indent=2) + "\n", encoding="utf-8", newline="\n")
    audit["graph_scan"] = "Vinc Fruit Fly: all base and derived values queried individually before registration; no keyword rows or literal node matches, fts+vector operational. Semantic neighbors are not literal seed hits."
    audit["date"] = "2026-10-09"
    (ROOT / "experiments/hold/hold_seed_registration.json").write_text(
        json.dumps(audit, indent=2) + "\n", encoding="utf-8", newline="\n")
    specs = [
        ("branch-exposure", "decision:hold-branch-exposure-d0-open", """All eight RECOMMENDED options in v1 section 12 are confirmed. D0 precedes any new condition. W1Dp is a design candidate only. E1 requires a later opening after D0 and is not opened here. No constructed witnesses now. The exposure screen remains 40 of 400, lost rows in [20, 380].

Implementation readings fixed before the run: the W1Dp/W1N expectations are conditional on the recorded B2 sensing positions, with no random draws. Burst/tie expectations may be computed by an exact finite-state recursion for the two most recent whiffs. They are proxies, not probabilities for a freely running new world. The draft supplies no calibrated mapping to P(X3): report observed identity split with its denominator, null if no eligible observation, and a conservative bound P(at least 40 exposed rows) <= expected tied-single opportunities / 40, capped at 1. Do not invent an exposure probability when the identity split or changed-state distribution is unmeasured. A bound failure in section 3 is reported and stops the branch conclusion; an unresolved proxy does not authorize E1.

Runtime: local Python 3.13.12, numpy 2.5.3, one process and BLAS threads 1. The existing passive instrument, fly.py, ph chain and seed pins stay byte-pinned. D0 uses the spent evaluation aliases only; no new experimental seed is consumed."""),
        ("stage2-coverage", "decision:hold-stage2-coverage-open", """All ten RECOMMENDED options in v1 section 12 are confirmed: A5 and B3, T1 only, ReadOutFly actual/instant, identities I1-I7 including I6, negative-source dwell R-H as primary with its lower interval bound strictly above 0, P(V) H-R lower bound at least -0.05, lost rows reported, span at least 1.0 on the bench, pass-probability stops at 0.5, A6 reported only, no draw tape. No materiality-bar selection is pending. Bench stops end that condition before development; no tuning, extensions or evaluation repeats.

Implementation corrections fixed before any run: I2 lists NINE nonlearning rows A1-A6 and B1-B3; the words 'all eleven' in v1 include the two excluded learning rows and are corrected. I4 compares available trajectory and score fields, with unrecorded TURN/EST captured by taps. For I5, each row's instantaneous identity and projected command are checked up to and including its first post-step state/field divergence, while its pre-step state and sensory inputs agree. A first command difference that occurs only after latent state divergence has no stage-one coupled projection identity and is reported as outside that check, not as a failed identity or an equality claim. I2 and I3/I6 remain the zero-tolerance code controls. A genuine identity failure stops before any bench and is diagnosed before a correction/re-run.

Seeds: config/hold-stage2-seeds.json is the exact registration for bench, dev, eval and bootstrap, selected after the full repository digit-boundary scan and individual graph searches including the balance, cast, D_OFF and A3_OFF derived streams. Scan receipt: experiments/hold/hold_seed_registration.json. Identity checks reuse the spent aliases. Seeds are named by those config keys in reports.

Runtime: local Python 3.13.12, numpy 2.5.3, one process and BLAS threads 1. Every stage persists per-row evidence and source/config/design hashes. The reviewing session recomputes headline statistics from stored arrays before graph result registration. One evaluation only, on surviving conditions; A6 bench and evaluation are reported even if both benefit conditions stop."""),
    ]
    for stem, decision, amendment in specs:
        src = ROOT / f"notes/hold/2026-10-07-hold-{stem}-design-v1.md"
        original = src.read_text(encoding="utf-8")
        title = original.splitlines()[0].replace("v1 DRAFT", "v2 FINAL")
        text = f"{title}\n\nDate 2026-10-09. Status: **v2 FINAL, owner-confirmed before implementation and runs**. {decision}.\n\nOwner instruction, verbatim: '다음 권고안에 따라 작업 이어서진행한다.' (proceed with the recommended next work). The recommendations refer to both v1 section-12 lists reviewed in the preceding progress response.\n\n## Confirmed choices and implementation readings\n\n{amendment}\n\n## Preserved v1 specification\n\nThe v1 text below preserves the original proposal and alternatives for provenance. Its future-tense approval statements and section-12 alternatives are superseded by the confirmed choices above. No measured result is added to this FINAL.\n\n{original}\n"
        dest = ROOT / f"notes/hold/2026-10-09-hold-{stem}-design-v2.md"
        dest.write_text(text, encoding="utf-8", newline="\n")
        print(dest.relative_to(ROOT).as_posix(), hashlib.sha256(dest.read_bytes()).hexdigest())
    print("seed registration complete", audit["files"], "files scanned; no hits")


if __name__ == "__main__":
    main()
