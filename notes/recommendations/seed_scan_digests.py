"""R2 step 3, owner's clone: for every ph35/ph33 seed-scan hit, the manifest row fields of design rev 3 (7ef2070). Read only.

Run from the repository root:  python notes/recommendations/seed_scan_digests.py
Writes notes/recommendations/2026-10-07-r2-step3-owner-entries.json (rows sorted by (checker, path, alias)) and prints a digit-free
summary. Seeds by alias; sha256 as 64 letters a-p (nibble n -> chr(ord('a') + n)); no seed digit anywhere in the output."""
import hashlib, json, os, re, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src")); os.chdir(REPO)
if callable(getattr(sys.stdout, "reconfigure", None)): sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import ph33, ph35

BASE = ["dev_w", "dev_a", "eval_w", "eval_a", "bench_w", "bench_a", "boot"]
LABELS = {"ph35": BASE + ["dev_w+10k", "eval_w+10k", "bench_w+10k", "dev_a+20k", "eval_a+20k", "bench_a+20k", "dev_w+20k", "eval_w+20k",
                          "bench_w+20k", "bench_w+10M", "bench_a+20M"],
          "ph33": BASE + ["dev_w+10k", "eval_w+10k", "bench_w+10k", "dev_w+D_OFF", "eval_w+D_OFF", "bench_w+D_OFF", "dev_a+20k", "eval_a+20k",
                          "bench_a+20k", "dev_a+A3_OFF", "eval_a+A3_OFF", "bench_a+A3_OFF", "dev_w+20k", "eval_w+20k", "bench_w+20k",
                          "bench_w+10M", "bench_a+20M"]}
QUOTED = {"experiments/h12/h12_design_v1.md", "experiments/h12/h12_design_v2.md", "experiments/h29/h29_design_v1.md", "experiments/h29/h29_design_v2.md"}
LOCAL = {"experiments/h18/arrays_b/K5b_restart_rand.npz", "notes/reviews/remote-runs/36260387653-summary/diagnosis/summary.json",
         "notes/reviews/remote-runs/36260387653/h12-remote-36260387653-1/diagnosis/summary.json",
         "notes/reviews/remote-runs/36261176952-summary/diagnosis/summary.json"}
ap = lambda digest_hex: "".join(chr(ord("a") + int(c, 16)) for c in digest_hex)
assert ap("0f") == "ap" and len(ap(hashlib.sha256(b"").hexdigest())) == 64

rows = []
for name, mod in (("ph35", ph35), ("ph33", ph33)):
    nums = mod.seed_numbers(); labs = LABELS[name]
    if len(nums) != len(labs): sys.exit(f"{name}: seed list length changed, aliases need review")
    alias = {n: l for n, l in zip(nums, labs) if n not in dict(zip(nums[:nums.index(n)], labs))}   # first alias per distinct number
    hits, _, nf = mod.seeds_unused()
    files = sorted((h if isinstance(h, str) else h[0]).replace("\\", "/") for h in hits)
    print(f"== {name}: {nf} files scanned, {len(files)} files hit")
    for rel in files:
        data = open(rel, "rb").read()                       # one buffer: the digest and every count come from these bytes
        digest = ap(hashlib.sha256(data).hexdigest())
        for n in dict.fromkeys(nums):
            k = len(re.findall(rb"(?<!\d)" + str(n).encode() + rb"(?!\d)", data))
            if k: rows.append(dict(checker=name, path=rel, alias=alias[n], occurrences=k, file_sha256_ap=digest,
                                   reason="historical_quotation" if rel in QUOTED else "incidental_match",
                                   presence="owner_local_optional" if rel in LOCAL else "required"))
rows.sort(key=lambda r: (r["checker"], r["path"], r["alias"]))
out = "notes/recommendations/2026-10-07-r2-step3-owner-entries.json"
with open(out, "w", encoding="utf-8", newline="\n") as f: json.dump(rows, f, indent=1, ensure_ascii=False); f.write("\n")
by = lambda c: [r for r in rows if r["checker"] == c]
print(f"rows: ph35 {len(by('ph35'))} pairs / {sum(r['occurrences'] for r in by('ph35'))} occurrences in {len({r['path'] for r in by('ph35')})} files;"
      f" ph33 {len(by('ph33'))} pairs / {sum(r['occurrences'] for r in by('ph33'))} occurrences in {len({r['path'] for r in by('ph33')})} files;"
      f" union {len({r['path'] for r in rows})} files")
assert (len(by("ph35")), len(by("ph33")), len({r["path"] for r in rows})) == (17, 25, 12), "pair counts differ from record:r2-step1-seed-scan-pairs-result"
assert all(r["alias"] in BASE[:5] for r in rows), "a derived or extra alias hit"
same = {r["path"]: r["file_sha256_ap"] for r in rows}
print("digests per file:"); [print(f"  {p} {d}") for p, d in sorted(same.items())]
print("wrote", out)
