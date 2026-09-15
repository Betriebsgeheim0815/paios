import subprocess
import sys
import unittest
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

if __name__=='__main__': unittest.main()
