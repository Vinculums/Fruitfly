#!/usr/bin/env python3
"""Read two fixed Vinc canonical documents without writes or scientific execution."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import urllib.error
import urllib.parse
import urllib.request

SPACE = "01a0b944-ecb4-737b-b3e6-5cc99ff37654"
HOST = "https://mcp.vincs.io"
DOCUMENTS = (
    ("d0d04637cd9ba7a6b", "notes/handoffs/2026-10-10-codex-cloud-handoff.md"),
    ("d60929b82c419fa4b", "experiments/h17/h17_run3_dev_report.md"),
)
AP = str.maketrans("0123456789abcdef", "abcdefghijklmnop")
MAX_RESPONSE_BYTES = 2 * 1024 * 1024


class RefuseRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "redirect refused", headers, fp)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().translate(AP)


def check(root: Path, opener=None, environ=None) -> dict:
    env = os.environ if environ is None else environ
    token = env.get("VINC_SK")
    result = {"format": "fruitfly-cloud-vinc-read-v1", "space": SPACE,
              "complete": False, "vinc_read_ready": False,
              "credential_required": not bool(token), "documents": []}
    if not token:
        result["reason"] = "VINC_SK is missing or empty"
        return result
    if opener is None:
        opener = urllib.request.build_opener(RefuseRedirect())
    for doc_id, local_path in DOCUMENTS:
        receipt = {"doc_id": doc_id, "local_path": local_path, "verified": False,
                   "canonical_text_matches": False}
        result["documents"].append(receipt)
        url = HOST + "/v1/documents/" + doc_id + "?" + urllib.parse.urlencode({"space": SPACE})
        try:
            # The destination is fixed; redirects are refused before another
            # request can be constructed with the authorization header.
            request = urllib.request.Request(url, headers={"Authorization": "Bearer " + token,
                                                          "Accept": "application/json"})
            with opener.open(request, timeout=30) as response:
                status = response.status
                receipt["http_status"] = status
                if status != 200:
                    receipt["reason"] = "unexpected HTTP status"
                    continue
                raw = response.read(MAX_RESPONSE_BYTES + 1)
                if len(raw) > MAX_RESPONSE_BYTES:
                    receipt["reason"] = "canonical response exceeds size limit"
                    continue
            document = json.loads(raw)
            if not isinstance(document, dict) or document.get("verified") is not True:
                receipt["reason"] = "canonical integrity verification absent or false"
                continue
            text = document.get("text")
            if not isinstance(text, str):
                receipt["reason"] = "canonical text missing"
                continue
            receipt["verified"] = True
            receipt["canonical_text_sha256_alpha"] = digest(text)
            # Universal newline handling matches canonical document publication.
            local_text = (root / local_path).read_text(encoding="utf-8")
            receipt["local_text_sha256_alpha"] = digest(local_text)
            receipt["canonical_text_matches"] = text == local_text
            if not receipt["canonical_text_matches"]:
                receipt["reason"] = "canonical text differs from checked-out local text"
        except urllib.error.HTTPError as error:
            receipt["http_status"] = error.code
            receipt["reason"] = ("redirect refused" if 300 <= error.code < 400
                                 else "HTTP access failure; authentication or network cause unverified")
        except Exception as error:
            # Exception messages, error bodies, tokens and headers are never
            # serialized: transport errors can include confidential values.
            receipt["reason"] = "read failed"
            receipt["exception_class"] = type(error).__name__
    result["complete"] = len(result["documents"]) == len(DOCUMENTS)
    result["vinc_read_ready"] = result["complete"] and all(
        row["verified"] and row["canonical_text_matches"] for row in result["documents"])
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", help="new receipt under notes/handoffs; never overwrite")
    args = parser.parse_args(argv)
    result = check(args.root.resolve())
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        value = PurePosixPath(args.output)
        output = (args.root / args.output).resolve()
        try:
            if (value.is_absolute() or ".." in value.parts or "\\" in args.output
                    or ":" in args.output or not output.is_relative_to(
                        (args.root / "notes/handoffs").resolve())):
                raise ValueError("invalid receipt path")
            with output.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(payload)
        except (OSError, ValueError):
            parser.error("receipt path unavailable, outside notes/handoffs, or already exists")
    print(payload, end="")
    if result["credential_required"]:
        return 2
    return 0 if result["vinc_read_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
