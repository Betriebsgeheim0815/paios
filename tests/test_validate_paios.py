import shutil
import tempfile
import unittest
from pathlib import Path
from tools.validate_paios import validate

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content, encoding="utf-8")

def fm(identifier, kind, extra=""):
    return f"---\nid: {identifier}\ntype: {kind}\ntitle: Test\ncreated: 2026-09-04\n{extra}---\n\nText\n"

class ValidatorTests(unittest.TestCase):
    def vault(self):
        root = Path(tempfile.mkdtemp()); self.addCleanup(shutil.rmtree, root)
        for folder in ("00_meta", "10_knowledge", "20_projects", "50_memory"): (root / folder).mkdir()
        write(root / "00_meta/paios.yaml", "version: 0.2\n")
        write(root / "00_meta/principles.md", fm("doc-principles", "meta"))
        write(root / "10_knowledge/k-2026-0001.md", fm("k-2026-0001", "knowledge", "source: https://example.test\n"))
        write(root / "20_projects/p-2026-0001.md", fm("p-2026-0001", "project", "status: active\nlinks: [k-2026-0001]\n"))
        write(root / "50_memory/m-2026-0001.md", fm("m-2026-0001", "memory", "scope: project\nproject: p-2026-0001\n"))
        return root
    def test_valid(self): self.assertFalse(validate(self.vault())[0])
    def test_duplicate_id(self):
        root = self.vault(); write(root / "10_knowledge/other.md", fm("k-2026-0001", "knowledge", "source: https://example.test\n")); self.assertTrue(any("nicht eindeutig" in x for x in validate(root)[0]))
    def test_missing_link(self):
        root = self.vault(); write(root / "20_projects/p-2026-0001.md", fm("p-2026-0001", "project", "status: active\nlinks: [k-2026-9999]\n")); self.assertTrue(any("links-Ziel" in x for x in validate(root)[0]))
    def test_invalid_memory(self):
        root = self.vault(); write(root / "50_memory/m-2026-0001.md", fm("m-2026-0001", "memory", "scope: project\n")); self.assertTrue(any("project-ID" in x for x in validate(root)[0]))
    def test_invalid_date(self):
        root = self.vault(); p = root / "10_knowledge/k-2026-0001.md"; write(p, p.read_text().replace("2026-09-04", "2026-99-99")); self.assertTrue(any("ISO-Datum" in x for x in validate(root)[0]))
