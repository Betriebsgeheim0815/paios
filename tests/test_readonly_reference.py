import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "mcp" / "readonly_reference.py"

class ReadonlyReferenceTests(unittest.TestCase):
    def test_read_finds_exact_id_in_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = root / "knowledge.md"
            entry.write_text("---\\nid: k-2026-0042\\ntype: knowledge\\ntitle: Found\\ncreated: 2026-01-01\\n---\\n\\n# Found\\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(root), "read", "k-2026-0042"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn("title: Found", result.stdout)
            self.assertNotIn("Not found", result.stdout)

if __name__ == "__main__":
    unittest.main()
