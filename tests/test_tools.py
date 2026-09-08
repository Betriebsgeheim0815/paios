import subprocess
import sys
import unittest

class ToolSmokeTests(unittest.TestCase):
    def test_cli_help(self):
        r=subprocess.run([sys.executable, 'tools/paios.py', '--help'],capture_output=True)
        self.assertEqual(r.returncode,0)

    def test_readonly_help(self):
        r=subprocess.run([sys.executable, 'mcp/readonly_reference.py', '--help'],capture_output=True)
        self.assertEqual(r.returncode,0)

if __name__=='__main__': unittest.main()
