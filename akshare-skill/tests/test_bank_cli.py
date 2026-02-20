import subprocess
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class TestBankCLI:
    """Test bank-related CLI commands"""

    def run_cli(self, *args):
        """Helper to run CLI command"""
        cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "akshare_cli.py")] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result

    def test_bank_fjcf_table_detail(self):
        """Test bank regulatory data"""
        result = self.run_cli(
            "bank_fjcf_table_detail",
            "--page", "1",
            "--item", "分局本级"
        )
        assert result.returncode == 0
