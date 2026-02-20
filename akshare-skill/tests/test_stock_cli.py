import subprocess
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class TestStockCLI:
    """Test stock-related CLI commands"""

    def run_cli(self, *args):
        """Helper to run CLI command"""
        cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "akshare_cli.py")] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result

    def test_stock_zh_a_hist(self):
        """Test historical stock data"""
        result = self.run_cli(
            "stock_zh_a_hist",
            "--symbol", "000001",
            "--start_date", "20240101",
            "--end_date", "20240115"
        )
        assert result.returncode == 0

    def test_stock_zh_a_spot(self):
        """Test stock realtime quotes"""
        result = self.run_cli(
            "stock_zh_a_spot",
            "--format", "json"
        )
        assert result.returncode == 0

    def test_index_zh_a_hist(self):
        """Test index historical data"""
        result = self.run_cli(
            "index_zh_a_hist",
            "--symbol", "000001",
            "--start_date", "20240101",
            "--end_date", "20240115"
        )
        assert result.returncode == 0
