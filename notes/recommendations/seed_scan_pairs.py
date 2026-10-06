"""R2 step 1: decompose the ph35 and ph33 seed-scan hits into (file, seed alias) pairs. Read only.

Run from the repository root on the machine that holds the working tree to be checked (the scan, like the
harnesses' own, walks the working tree, tracked or not):  python notes/recommendations/seed_scan_pairs.py
Seed values are shown by alias and every digit in a context is masked as '#'.
Console summary counts remain numeric; review summaries before copying into P5-covered documents."""
import os, re, sys
# Binary contexts may contain replacement characters unsupported by Windows cp949.
if callable(getattr(sys.stdout, "reconfigure", None)):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src")); os.chdir(REPO)
import ph33, ph35

BASE = ["dev_w", "dev_a", "eval_w", "eval_a", "bench_w", "bench_a", "boot"]
LABELS = {
    "ph35": BASE + ["dev_w+10k", "eval_w+10k", "bench_w+10k", "dev_a+20k", "eval_a+20k", "bench_a+20k",
                    "dev_w+20k", "eval_w+20k", "bench_w+20k", "bench_w+10M", "bench_a+20M"],
    "ph33": BASE + ["dev_w+10k", "eval_w+10k", "bench_w+10k", "dev_w+D_OFF", "eval_w+D_OFF", "bench_w+D_OFF",
                    "dev_a+20k", "eval_a+20k", "bench_a+20k", "dev_a+A3_OFF", "eval_a+A3_OFF", "bench_a+A3_OFF",
                    "dev_w+20k", "eval_w+20k", "bench_w+20k", "bench_w+10M", "bench_a+20M"],
}
mask = lambda s: re.sub(r"\d", "#", s)
union = {}
for name, mod in (("ph35", ph35), ("ph33", ph33)):
    nums = mod.seed_numbers(); labs = LABELS[name]
    if len(nums) != len(labs): sys.exit(f"{name}: seed list length changed, aliases need review")
    alias = {}
    for n, l in zip(nums, labs): alias.setdefault(n, []).append(l)
    hits, _, nf = mod.seeds_unused()
    files = sorted((h if isinstance(h, str) else h[0]).replace("\\", "/") for h in hits)
    print(f"== {name}: {len(set(nums))} distinct numbers, {nf} files scanned, {len(files)} files hit")
    for rel in files:
        union.setdefault(rel, set()).add(name)
        data = open(rel, "rb").read()
        for n in dict.fromkeys(nums):
            ms = list(re.finditer(rb"(?<!\d)" + str(n).encode() + rb"(?!\d)", data))
            if not ms: continue
            print(f"  {name} | {rel} | {'/'.join(alias[n])} | {len(ms)} occurrence(s) | reason: (owner)")
            for k, m in enumerate(ms[:3]):
                ctx = data[max(0, m.start() - 50):m.end() + 50].decode("utf-8", "replace").replace("\n", " ")
                print(f"      occurrence {k + 1}: ...{mask(ctx)}...")
print(f"== union: {len(union)} distinct files")
for rel in sorted(union): print(f"  {rel} | {', '.join(sorted(union[rel]))}")
