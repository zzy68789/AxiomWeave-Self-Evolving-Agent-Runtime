from __future__ import annotations

import os
import unittest
from pathlib import Path
from unittest.mock import patch

from agents import memory


class ProjectHashTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows-specific path normalization")
    def test_project_hash_ignores_path_case_on_windows(self) -> None:
        with patch.object(memory.Path, "cwd", return_value=Path(r"D:\Code\AxiomWeave")):
            upper_case_hash = memory._project_hash()

        with patch.object(memory.Path, "cwd", return_value=Path(r"D:\code\AxiomWeave")):
            lower_case_hash = memory._project_hash()

        self.assertEqual(upper_case_hash, lower_case_hash)


if __name__ == "__main__":
    unittest.main()
