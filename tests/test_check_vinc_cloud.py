"""Synthetic network fixtures; no live credential or canonical writes."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import urllib.error
import urllib.request

SPEC = importlib.util.spec_from_file_location(
    "check_vinc_cloud", Path(__file__).resolve().parents[1] / "tools/check_vinc_cloud.py")
vinc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(vinc)
TOKEN = "synthetic-private-token"


class Response:
    def __init__(self, value, status=200):
        self.status = status
        self.data = json.dumps(value).encode()

    def read(self, size):
        return self.data[:size]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class VincCloudTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for _, path in vinc.DOCUMENTS:
            destination = self.root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"fixture canonical\r\n")
        self.env = {"VINC_SK": TOKEN}
        self.opener = mock.Mock()
        self.opener.open.side_effect = lambda *args, **kwargs: Response(
            {"verified": True, "text": "fixture canonical\n"})

    def test_missing_credential_has_no_network_call(self):
        for value in ({}, {"VINC_SK": ""}):
            result = vinc.check(self.root, self.opener, value)
            self.assertTrue(result["credential_required"])
            self.assertFalse(result["vinc_read_ready"])
            self.assertFalse(result["complete"])
        self.opener.open.assert_not_called()

    def test_exact_verified_reads_and_fixed_destinations(self):
        result = vinc.check(self.root, self.opener, self.env)
        self.assertTrue(result["complete"])
        self.assertTrue(result["vinc_read_ready"])
        self.assertEqual(len(result["documents"]), len(vinc.DOCUMENTS))
        for call in self.opener.open.call_args_list:
            request = call.args[0]
            self.assertTrue(request.full_url.startswith(vinc.HOST + "/v1/documents/"))
            self.assertIn(vinc.SPACE, request.full_url)
        self.assertNotIn(TOKEN, json.dumps(result))

    def test_verified_false_and_nonboolean_are_not_accepted(self):
        for value in (False, "true", 1, None):
            self.opener.open.side_effect = lambda *args, **kwargs: Response(
                {"verified": value, "text": "fixture canonical\n"})
            result = vinc.check(self.root, self.opener, self.env)
            self.assertFalse(result["vinc_read_ready"])
            self.assertFalse(result["documents"][0]["verified"])

    def test_text_mismatch_keeps_verified_but_fails_access_readiness(self):
        self.opener.open.side_effect = lambda *args, **kwargs: Response(
            {"verified": True, "text": "different canonical text"})
        result = vinc.check(self.root, self.opener, self.env)
        self.assertFalse(result["vinc_read_ready"])
        self.assertTrue(result["documents"][0]["verified"])
        self.assertFalse(result["documents"][0]["canonical_text_matches"])

    def test_text_is_required(self):
        self.opener.open.side_effect = lambda *args, **kwargs: Response({"verified": True})
        self.assertFalse(vinc.check(self.root, self.opener, self.env)["vinc_read_ready"])

    def test_http_error_body_and_headers_are_not_serialized(self):
        self.opener.open.side_effect = urllib.error.HTTPError(
            vinc.HOST, 403, TOKEN, {"Authorization": TOKEN}, io.BytesIO(TOKEN.encode()))
        result = vinc.check(self.root, self.opener, self.env)
        payload = json.dumps(result)
        self.assertNotIn(TOKEN, payload)
        self.assertFalse(result["vinc_read_ready"])
        self.assertEqual(result["documents"][0]["http_status"], 403)
        self.assertIn("unverified", result["documents"][0]["reason"])

    def test_exception_message_is_never_serialized(self):
        self.opener.open.side_effect = RuntimeError(TOKEN)
        result = vinc.check(self.root, self.opener, self.env)
        self.assertNotIn(TOKEN, json.dumps(result))
        self.assertEqual(result["documents"][0]["exception_class"], "RuntimeError")

    def test_redirect_handler_refuses_without_constructing_new_request(self):
        handler = vinc.RefuseRedirect()
        request = urllib.request.Request(vinc.HOST, headers={"Authorization": "Bearer " + TOKEN})
        with self.assertRaises(urllib.error.HTTPError) as raised:
            handler.redirect_request(request, io.BytesIO(), 302, "moved", {}, "https://outside.test")
        self.assertEqual(raised.exception.code, 302)
        self.opener.open.side_effect = raised.exception
        result = vinc.check(self.root, self.opener, self.env)
        self.assertEqual(result["documents"][0]["reason"], "redirect refused")
        self.assertNotIn(TOKEN, json.dumps(result))

    def test_non_ok_status_fails(self):
        self.opener.open.side_effect = lambda *args, **kwargs: Response({}, status=202)
        self.assertFalse(vinc.check(self.root, self.opener, self.env)["vinc_read_ready"])

    def test_cli_missing_credential_exit_and_exclusive_receipt(self):
        (self.root / "notes/handoffs").mkdir(parents=True, exist_ok=True)
        argv = ["--root", str(self.root), "--output", "notes/handoffs/fixture.json"]
        with mock.patch.dict(vinc.os.environ, {}, clear=True), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(vinc.main(argv), 2)
        self.assertTrue(json.loads(out.getvalue())["credential_required"])
        with mock.patch.dict(vinc.os.environ, {}, clear=True), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                vinc.main(argv)
            with self.assertRaises(SystemExit):
                vinc.main(["--root", str(self.root), "--output", "config/out.json"])


if __name__ == "__main__":
    unittest.main()
