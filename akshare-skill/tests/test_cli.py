import pytest
import subprocess
import json
import sys
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent


class TestAKShareCLI:
    """Test AKShare CLI wrapper"""

    def run_cli(self, *args):
        """Helper to run CLI command"""
        cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "akshare_cli.py")] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result

    def test_cli_help(self):
        """Test --help flag"""
        result = self.run_cli("--help")
        assert result.returncode == 0
        assert "Usage" in result.stdout

    def test_macro_china_gdp_pretty(self):
        """Test macro_china_gdp with pretty format"""
        result = self.run_cli("macro_china_gdp", "--format", "pretty")
        assert result.returncode == 0
        assert len(result.stdout) > 0

    def test_macro_china_gdp_json(self):
        """Test macro_china_gdp with JSON format"""
        result = self.run_cli("macro_china_gdp", "--format", "json")
        assert result.returncode == 0
        # Verify valid JSON
        data = json.loads(result.stdout)
        assert isinstance(data, list)

    def test_invalid_function(self):
        """Test error handling for invalid function"""
        result = self.run_cli("nonexistent_function")
        assert result.returncode != 0
        assert "not found" in result.stderr or "Error" in result.stderr

    def test_missing_required_param(self):
        """Test error handling for missing required parameters"""
        # stock_zh_a_hist requires symbol, start_date, end_date
        result = self.run_cli("stock_zh_a_hist")
        assert result.returncode != 0

    def test_stock_zh_a_hist(self):
        """Test stock_zh_a_hist with parameters"""
        result = self.run_cli(
            "stock_zh_a_hist",
            "--symbol", "000001",
            "--start_date", "20240101",
            "--end_date", "20240110",
            "--format", "csv"
        )
        assert result.returncode == 0
        # Should contain CSV header and data
        lines = result.stdout.strip().split('\n')
        assert len(lines) > 1

    def test_bank_fjcf_table_detail(self):
        """Test bank_fjcf_table_detail with parameters"""
        result = self.run_cli(
            "bank_fjcf_table_detail",
            "--page", "1",
            "--item", "分局本级",
            "--format", "json"
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, list)
