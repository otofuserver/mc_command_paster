from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class SmokeTest(unittest.TestCase):
    def test_dry_run(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        command_file = repo_root / "examples" / "smoke_commands.txt"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "mc_command_paster",
                str(command_file),
                "--dry-run",
                "--countdown",
                "10",
                "--delay-ms",
                "500",
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("[DRY-RUN]", result.stdout)


if __name__ == "__main__":
    unittest.main()

