import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))
from paios_proposals import create_proposal, save_proposal, validate_proposal


class ProposalTests(unittest.TestCase):
    def test_create_contains_actor_revision_and_sources(self):
        proposal = create_proposal("k-2026-0001", "update", {"title": "Neu"}, "model:example", 3, ["src-1"], "Quelle verarbeitet")
        self.assertTrue(proposal["proposal_id"].startswith("prop-"))
        self.assertEqual(proposal["actor"], "model:example")
        self.assertEqual(proposal["base_revision"], 3)
        self.assertEqual(validate_proposal(proposal), [])

    def test_invalid_revision_is_rejected(self):
        with self.assertRaises(ValueError):
            create_proposal("k-2026-0001", "update", {}, "model:example", -1)

    def test_save_creates_pending_proposal_file(self):
        with tempfile.TemporaryDirectory() as directory:
            proposal = create_proposal("p-2026-0001", "archive", {}, "human:owner", 2)
            path = save_proposal(directory, proposal)
            self.assertTrue(path.is_file())
            self.assertEqual(path.parent.name, "proposals")
            self.assertIn("\"status\": \"pending\"", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
