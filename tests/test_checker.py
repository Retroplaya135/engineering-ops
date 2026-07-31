import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_record", ROOT / "tools/check-record.py")
check_record = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(check_record)


class WorkRecordTests(unittest.TestCase):
    def test_examples_are_valid(self):
        for path in sorted((ROOT / "examples").glob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(check_record.validate(record), [], path)

    def test_every_required_field_is_enforced(self):
        record = json.loads((ROOT / "examples/routine.json").read_text(encoding="utf-8"))
        for field in check_record.REQUIRED:
            invalid = dict(record)
            del invalid[field]
            self.assertIn(f"missing field: {field}", check_record.validate(invalid))

    def test_evidence_shape_is_enforced(self):
        record = json.loads((ROOT / "examples/routine.json").read_text(encoding="utf-8"))
        record["evidence"] = [{"claim": "proof"}]
        self.assertTrue(check_record.validate(record))


if __name__ == "__main__":
    unittest.main()
