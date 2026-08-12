import json
import unittest
from pathlib import Path

from scripts.reference_kpis import calculate_reference_kpis

ROOT = Path(__file__).resolve().parents[1]


class ReferenceKpiTests(unittest.TestCase):
    def test_reference_results_match_reviewed_snapshot(self) -> None:
        expected = json.loads((ROOT / "tests/expected-kpis.json").read_text())
        self.assertEqual(calculate_reference_kpis(ROOT), expected)

    def test_security_identities_are_non_routable(self) -> None:
        access_rows = (ROOT / "data/sample-security-access.csv").read_text().splitlines()[1:]
        identities = [row.split(",", 1)[0] for row in access_rows]
        self.assertTrue(identities)
        self.assertTrue(all(identity.endswith("@example.invalid") for identity in identities))


if __name__ == "__main__":
    unittest.main()
