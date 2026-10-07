#!/usr/bin/env python3
"""Scan-only R2 verification. No experiment, demo, or behavioral acceptance."""
import ast
import hashlib
import importlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "config/seed-scan-exceptions-r2.json"
DECISION = "decision:seed-scan-exception-pairs-r2"
MANIFEST_PIN = 'gkkeiinehcdkdajmgdhpcagkffdhjojkglbljnmefphakmogknnljmloeaacligg'
# Approved source bytes, including the local import closure. No runtime override.
SOURCE_PINS = {'ffcore': 'aoieidgcfenmalkbdjdgnilihpmkjgedcohdpbnlneolebpdjgfaamfemjbhofdh',
 'ph10': 'nojdpbhhmnfpfccfpnfogcabbgfimcffjhddikfkmcnhkdbofjhpbfjblgdeaelk',
 'ph11': 'oiapealnhbakmkedcfcpaedcjiegppkcjjedcfbnbjohbiefaojkhppejojehkcd',
 'ph12': 'obadfoajimdlicijjiljjlafpijlhodlilmkbfpdacfddokchpmmebdjlkndkbmh',
 'ph12b': 'omglbijgpgaopcocfanajcoapjpjpebafmagldipgjjinojahaamkdhbcbdoapkk',
 'ph13': 'cnhfpkoioimdbobmgnnpgfhhhicpkpnodajjpbapoipfapodicpfdnajojopbpcn',
 'ph14': 'mglhefmgapjjjcjdekammlmffieopdfekadpfdpaildhkbcfckgjepoldfaloana',
 'ph14b': 'opbioppiddmmpbgaandjhfinhckfalpghanhncabdncbdhnenbggadpagnbfdbco',
 'ph15': 'mmjdjjjgfofmlmdamlhpdfoimocjgninedoegfhmpgeenbomdfajdbofjeeadpnm',
 'ph16': 'ddnfpnlcfjfjplhpjmloegfmkcfkijhdhhgldjpbofbhangefmlfdlminjagkcmc',
 'ph17': 'eldannpilbpmgnmfbapcdkcipajngdjbaadnjfpaheedeencdhpfaoddjdkdgijp',
 'ph18': 'cgknenoplhfjaobgobadalalgpiahdndcfifielkoomaglkggocdddbfnkhmjhmd',
 'ph19': 'aamgkdldcpiapkojpfilgnlncdkioadlbhbaloefpmpddfcdipcijfghpmodehjb',
 'ph2': 'joaopiddndpfjfhnkdebmpoljonnhhpojknlbbnofdfemhbbgcmhfgjoidodakek',
 'ph20': 'onomgnideigammgmemakmdgbjjipoajeafdeelcoejekopcbkcilaemkhlgmoplo',
 'ph20b': 'elgmaejhjhgeglbhpoigdcbafdhagjgdmbmgepgpfbabiphikfkefcpheomnejnb',
 'ph21': 'dkbnhjnjkancdfpblophoedfomfjemppeaeibiaochlcinmnijcfjimfiebdmpmb',
 'ph22': 'adklimehaglbjffhkpfngeonnidpibckllkjblgbiedjgbildfidhkejnneemkbm',
 'ph23': 'kobiaejcoomojdhdjnkenblfnidkbdkclecmfojfceefkjcklhfpjfmgplcolfko',
 'ph24': 'pdeepbhiocadiaifipenheaaopghaccdpjakkcjchldphdaehhckobnieilnblop',
 'ph25': 'fgcakjaibjgjddhjkfddhemkdiebodlmdnnlkiganikidfbnkhkkbonenpobhnjb',
 'ph25b': 'knbckjbccmbhbnndcmdpmokmjegknnjnaoladiaoiifoapaihcnnjhmmnfjookpg',
 'ph28': 'gemohnamobcdpjbckkghfoiggchnflglakodnijjhglajdgggdbgoglhieebohkk',
 'ph29': 'bccmbjcfaokfnghnanlnjjhpkcaejdmgdmgmbbabpkppidndmmgldojahnemhjjm',
 'ph3': 'aledngpdnjllihldidnidgjcjhohleedhiibfbejcfgdphhfgbpeiknfmofhdpol',
 'ph30': 'jiiccideaednofpdbgbfohdmnekideeeknmopcpbnfofgehidfgnhamkjafafjln',
 'ph32': 'njpfifnffjjokjkepcbioihlniiepkicegkicgloabbbpejfmplomcjjkjccched',
 'ph33': 'pckcjhcckdjimiblhphdabencjmhjjkaimcijomkbmmhdggkmngfofabfeohcala',
 'ph34b': 'bnohabghmblnnnahkffjmhdaddpdgiglfpphbnldncminnggcnkmiaieahpdlpcf',
 'ph35': 'oekdmonkcfgciohacgkgeigbknfbpiejhepbockhcahjechgnphagnaagkfclblb',
 'ph36': 'lidlnjojnblnjlbjbnhhbhhjlbmnjahnjolafhhjhbafmafoickmlbfnckjjmkhb',
 'ph36b': 'mpljkcgkeflpnfopjofnhibnhdkhhcodbcjnlceogddmggoolijmcngbffgpbmop',
 'ph38': 'jepcpedkcdabcgmngedbedbegmdflljhhpkmaeapkhaeleopobfhfadmaelfjnaf',
 'ph4': 'naajfgimnkenlkdfipbifhcgiocbkbafkniokmbaknnggfleahjcmbmiccdigegk',
 'ph8': 'knkcpmeldimjnaaidnaidgghkodplolgbfpfeelefpiabjjomflclmigogndledo',
 'ph9': 'hgjjleogplehkbloofphoeojjbkiikkmipkfkpdkjeacjhplneoeebeebpenjhag'}
OPTIONAL_PATHS = frozenset(['experiments/h18/arrays_b/K5b_restart_rand.npz',
 'notes/reviews/remote-runs/36260387653-summary/diagnosis/summary.json',
 'notes/reviews/remote-runs/36260387653/h12-remote-36260387653-1/diagnosis/summary.json',
 'notes/reviews/remote-runs/36261176952-summary/diagnosis/summary.json'])
ALIASES = {"dev_w", "dev_a", "eval_w", "eval_a", "bench_w"}
ROW_FIELDS = {"checker", "path", "alias", "occurrences", "file_sha256_ap", "reason", "presence"}


class VerificationError(Exception):
    pass


def digest_ap(data):
    return hashlib.sha256(data).hexdigest().translate(
        str.maketrans("0123456789abcdef", "abcdefghijklmnop"))


def decode_digest(value):
    if not isinstance(value, str) or re.fullmatch("[a-p]{64}", value) is None:
        raise VerificationError("invalid digest encoding")
    return bytes.fromhex(value.translate(str.maketrans("abcdefghijklmnop", "0123456789abcdef")))


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise VerificationError("duplicate JSON key")
        obj[key] = value
    return obj


def load_manifest(root):
    raw = (root / MANIFEST).read_bytes()
    if hashlib.sha256(raw).digest() != decode_digest(MANIFEST_PIN):
        raise VerificationError("manifest pin mismatch")
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise VerificationError("manifest byte format")
    document = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    if not isinstance(document, dict) or set(document) != {"schema", "decision", "entries"}:
        raise VerificationError("manifest fields")
    if document["schema"] != "r2-v1" or document["decision"] != DECISION:
        raise VerificationError("manifest schema or decision")
    entries = document["entries"]
    if not isinstance(entries, list) or not entries:
        raise VerificationError("manifest entries")
    keys = []
    for row in entries:
        if not isinstance(row, dict) or set(row) != ROW_FIELDS:
            raise VerificationError("row fields")
        if any(not isinstance(row[k], str) for k in ROW_FIELDS - {"occurrences"}):
            raise VerificationError("row field type")
        if row["checker"] not in {"ph33", "ph35"} or row["alias"] not in ALIASES:
            raise VerificationError("checker or alias")
        path = row["path"]
        if (not path or PurePosixPath(path).is_absolute() or
                any(p in {"", ".", ".."} for p in path.split("/")) or
                any(c in path for c in "\\*?[]:") or any(ord(c) < 32 for c in path)):
            raise VerificationError("invalid relative path")
        if type(row["occurrences"]) is not int or row["occurrences"] <= 0:
            raise VerificationError("invalid occurrence count")
        decode_digest(row["file_sha256_ap"])
        if row["reason"] not in {"historical_quotation", "incidental_match"}:
            raise VerificationError("invalid reason")
        expected = "owner_local_optional" if path in OPTIONAL_PATHS else "required"
        if row["presence"] != expected:
            raise VerificationError("invalid presence")
        keys.append((row["checker"], path, row["alias"]))
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise VerificationError("unsorted or duplicate rows")
    return entries


def recorded_value(root, module, variable):
    tree = ast.parse((root / "src" / (module + ".py")).read_bytes())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == variable for t in node.targets):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "dict":
                return {k.arg: ast.literal_eval(k.value) for k in node.value.keywords}
            return ast.literal_eval(node.value)
    raise VerificationError("missing legacy pin")


def verify_sources(root):
    for name, pin in SOURCE_PINS.items():
        if hashlib.sha256((root / "src" / (name + ".py")).read_bytes()).digest() != decode_digest(pin):
            raise VerificationError("source pin mismatch: " + name)
    ph32 = hashlib.sha256((root / "src/ph32.py").read_bytes()).hexdigest()
    ph35 = hashlib.sha256((root / "src/ph35.py").read_bytes()).hexdigest()
    if recorded_value(root, "ph33", "PH32_SHA") != ph32:
        raise VerificationError("legacy ph32 pin mismatch")
    if recorded_value(root, "ph36b", "SHA_ON_RECORD")["ph35"] != ph35:
        raise VerificationError("downstream full pin mismatch")
    if not ph35.startswith(recorded_value(root, "ph38", "REGISTERED")["ph35"]):
        raise VerificationError("downstream prefix pin mismatch")


def aliases_for(checker):
    aliases = dict(dev_w=checker.SEEDS["dev"][0], dev_a=checker.SEEDS["dev"][1],
                   eval_w=checker.SEEDS["eval"][0], eval_a=checker.SEEDS["eval"][1],
                   bench_w=checker.BENCH["seed_w"])
    if len(set(aliases.values())) != len(aliases) or not set(aliases.values()) <= set(checker.seed_numbers()):
        raise VerificationError("seed alias definitions changed")
    return aliases


def count_number(data, number):
    return len(re.findall(rb"(?<!\d)" + str(number).encode("ascii") + rb"(?!\d)", data))


def scan_checker(root, name, checker, entries):
    aliases = aliases_for(checker)
    # Call the original checker without replacing functions, constants, or traversal.
    hits, nums, nf = checker.seeds_unused()
    if nums != checker.seed_numbers():
        raise VerificationError("checker seed return changed")
    rows = [r for r in entries if r["checker"] == name]
    buffers = {}
    errors = []
    valid = set()
    unused = []

    def read(path):
        if path not in buffers:
            buffers[path] = (root / path).read_bytes()
        return buffers[path]

    for row in rows:
        path, alias = row["path"], row["alias"]
        try:
            data = read(path)
        except FileNotFoundError:
            if row["presence"] == "owner_local_optional":
                unused.append(dict(path=path, alias=alias, status="absent/unused"))
            else:
                errors.append("required file missing: " + path)
            continue
        except OSError:
            errors.append("registered file unreadable: " + path)
            continue
        if (hashlib.sha256(data).digest() != decode_digest(row["file_sha256_ap"]) or
                count_number(data, aliases[alias]) != row["occurrences"]):
            errors.append("expired row: " + path + " / " + alias)
        else:
            valid.add((path, aliases[alias]))

    applied = set()
    hit_pairs = 0
    for hit in hits:
        path = hit[0] if name == "ph33" else hit
        data = read(path)
        if name == "ph33":
            numbers = [n for n in nums if (path, n) not in checker.ph32.EXCLUDED_PAIRS
                       and count_number(data, n)]
            if set(numbers) != set(hit[1]):
                errors.append("hit file changed during scan: " + path)
        else:
            # ph35 returns file names only. Preserve its one existing pair exclusion.
            pair = ("experiments/h20/ph31_eval.txt", checker.ph30.SEEDS["eval"][0][1])
            numbers = [n for n in nums if (path, n) != pair and count_number(data, n)]
        if not numbers:
            errors.append("hit file changed during scan: " + path)
        for number in numbers:
            hit_pairs += 1
            if (path, number) in valid:
                applied.add((path, number))
            else:
                errors.append("uncovered hit in " + path)
    if valid - applied:
        errors.append("registered rows no longer returned by original scan")
    return dict(checker=name, scanned_files=nf, hit_files=len(hits), hit_pairs=hit_pairs,
                applied_rows=len(applied), unused=unused, errors=errors)


def run():
    if not __debug__ or sys.flags.optimize:
        raise VerificationError("assertions must be enabled")
    verify_sources(ROOT)
    entries = load_manifest(ROOT)
    sys.path.insert(0, str(ROOT / "src"))
    results = []
    for name in ("ph33", "ph35"):
        checker = importlib.import_module(name)
        if Path(checker.__file__).resolve() != ROOT / "src" / (name + ".py"):
            raise VerificationError("unexpected checker import")
        results.append(scan_checker(ROOT, name, checker, entries))
    report = dict(command="python tools/verify_seed_scan_r2.py",
                  verifier_sha256_ap=digest_ap(Path(__file__).read_bytes()),
                  manifest_sha256_ap=MANIFEST_PIN, source_pins="PASS", downstream_pins="PASS",
                  measurement="N/A", behavior="N/A", checks=results,
                  local_coverage="incomplete" if any(r["unused"] for r in results) else "present files checked")
    print(json.dumps(report, indent=2))
    return int(any(r["errors"] for r in results))


if __name__ == "__main__":
    try:
        sys.exit(run())
    except (VerificationError, OSError, ValueError, ImportError) as exc:
        # Do not echo input bytes, seed values, or parser excerpts into reports.
        print("R2 verification failed: " + (str(exc) if isinstance(exc, VerificationError) else type(exc).__name__), file=sys.stderr)
        sys.exit(1)
