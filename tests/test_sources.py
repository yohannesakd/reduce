import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent


class SourcesTest(unittest.TestCase):
    def test_the_skill_cites_only_copied_sources_and_every_link_resolves(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/sources.py"), "check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
