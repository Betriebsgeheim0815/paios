import subprocess
import sys
import unittest
import tempfile
from pathlib import Path

class ToolSmokeTests(unittest.TestCase):
    ROOT = Path(__file__).parents[1]

    def test_cli_help(self):
        r=subprocess.run([sys.executable, str(self.ROOT / 'tools/paios.py'), '--help'],capture_output=True, cwd=self.ROOT)
        self.assertEqual(r.returncode,0)

    def test_readonly_help(self):
        r=subprocess.run([sys.executable, str(self.ROOT / 'mcp/readonly_reference.py'), '--help'],capture_output=True, cwd=self.ROOT)
        self.assertEqual(r.returncode,0)

    def test_python_sources_compile(self):
        sources = list(self.ROOT.glob('tools/*.py')) + list(self.ROOT.glob('mcp/*.py'))
        for source in sources:
            with self.subTest(source=source.name):
                compile(source.read_text(encoding='utf-8'), str(source), 'exec')

    def test_backfill_dry_run_does_not_modify_legacy_file(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory) / 'vault' / '10_knowledge'
            vault.mkdir(parents=True)
            legacy = vault / 'old-note.md'
            legacy.write_text('# Legacy\n', encoding='utf-8')
            result = subprocess.run(
                [sys.executable, str(self.ROOT / 'tools/backfill_frontmatter.py'),
                 str(vault.parent), '--dry-run'],
                capture_output=True, text=True, cwd=self.ROOT,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn('WOULD ADD', result.stdout)
            self.assertEqual(legacy.read_text(encoding='utf-8'), '# Legacy\n')

if __name__=='__main__': unittest.main()
