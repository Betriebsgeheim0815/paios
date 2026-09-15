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

if __name__=='__main__': unittest.main()
