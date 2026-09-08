import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

class ValidatorTests(unittest.TestCase):
    def base(self):
        root = Path(tempfile.mkdtemp())
        for name in ['00_meta','10_knowledge','20_projects','50_memory']: (root/name).mkdir(parents=True)
        (root/'00_meta/paios.yaml').write_text('name: test\n')
        (root/'00_meta/principles.md').write_text('---\nid: doc-principles\ntype: meta\ntitle: Principles\ncreated: 2026-01-01\n---\n')
        return root

    def run(self, root):
        return subprocess.run([sys.executable,'tools/validate_paios.py',str(root)],capture_output=True,text=True)

    def test_valid_entry(self):
        root = self.base()
        (root/'10_knowledge/k-2026-0001.md').write_text('---\nid: k-2026-0001\ntype: knowledge\ntitle: Example\ncreated: 2026-01-02\n---\n')
        self.assertEqual(self.run(root).returncode,0)

    def test_duplicate_and_wrong_prefix_fail(self):
        root = self.base()
        text = '---\n id: k-2026-0001\ntype: project\ntitle: Bad\ncreated: 2026-01-02\nstatus: active\n---\n'.replace('\n id','\nid')
        for name in ['20_projects/a.md','20_projects/b.md']: (root/name).write_text(text)
        self.assertNotEqual(self.run(root).returncode,0)

if __name__ == '__main__': unittest.main()
