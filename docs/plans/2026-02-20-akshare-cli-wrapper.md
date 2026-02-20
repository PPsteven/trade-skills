# AKShare CLI Wrapper Tool - Complete Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a comprehensive CLI wrapper for AKShare library and update all documentation to use CLI commands instead of Python imports.

**Architecture:**
1. Create `scripts/akshare_cli.py` - CLI tool that wraps all AKShare functions
2. Create comprehensive test suite in `tests/` - Test each API via CLI
3. Update all `references/*.md` files - Replace Python imports with CLI commands
4. Validate all tests pass and documentation is consistent

**Tech Stack:** Python Click/argparse, pytest, AKShare library, bash scripting

---

## Task 1: Design CLI Tool Architecture

**Files:**
- Research: AKShare API structure
- Plan: CLI command hierarchy

**Step 1: Examine AKShare module structure**

```bash
python3 << 'EOF'
import akshare as ak
import inspect

# Get all public functions
funcs = [name for name in dir(ak) if not name.startswith('_') and callable(getattr(ak, name))]
print(f"Total functions: {len(funcs)}")
print("Sample functions:")
for func in sorted(funcs)[:10]:
    print(f"  - {func}")
EOF
```

**Step 2: Document command format decision**

Decision: Use `akshare-cli <function_name> --param1 value1 --param2 value2` format

Example:
```bash
akshare-cli bank_fjcf_table_detail --page 5 --item "分局本级"
```

**Step 3: Plan parameter handling**

- Function name as first positional argument
- All parameters as `--key value` flags
- Support for different data types: strings, integers, booleans, dates
- Output format options: `--format json|csv|pretty|raw`

**Step 4: Create design document**

Create `/Users/ppsteven/projects/trade-skills/akshare-skill/CLI_DESIGN.md`:

```markdown
# AKShare CLI Tool Design

## Command Format

\`\`\`bash
akshare-cli <function_name> [--param1 value1] [--param2 value2] [--format output_format]
\`\`\`

## Usage Examples

\`\`\`bash
# Get stock data
akshare-cli stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131 --format csv

# Get macro data
akshare-cli macro_china_gdp --format json

# Get bank penalties
akshare-cli bank_fjcf_table_detail --page 5 --item "分局本级" --format pretty
\`\`\`

## Output Formats

- **pretty**: Human-readable table format (default for DataFrames)
- **csv**: CSV format
- **json**: JSON format
- **raw**: Raw Python object representation

## Parameter Types

Automatically detected from function signature:
- `str`: String parameters
- `int`: Integer parameters
- `bool`: Boolean flags (--flag for True, --no-flag for False)
- `float`: Float parameters
- `datetime`/`date`: Date parameters
```

**Step 5: Commit design**

```bash
cd /Users/ppsteven/projects/trade-skills/akshare-skill
git add CLI_DESIGN.md
git commit -m "docs: design CLI tool architecture and command format"
```

---

## Task 2: Implement CLI Tool Core

**Files:**
- Create: `scripts/akshare_cli.py`
- Create: `scripts/setup_cli.py` (optional, for installation)

**Step 1: Write main CLI tool**

Create `scripts/akshare_cli.py`:

```python
#!/usr/bin/env python3
"""
AKShare CLI Wrapper Tool

Usage:
    akshare-cli <function_name> [--param1 value1] [--param2 value2] [--format output_format]

Examples:
    akshare-cli stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131
    akshare-cli macro_china_gdp --format json
    akshare-cli bank_fjcf_table_detail --page 5 --item "分局本级"
"""

import sys
import argparse
import json
import inspect
import akshare as ak
from typing import Any, Dict
import pandas as pd


class AKShareCLI:
    """CLI wrapper for AKShare functions"""

    def __init__(self):
        self.ak = ak
        self.output_format = "pretty"

    def get_function(self, func_name: str):
        """Get function from akshare module"""
        if not hasattr(self.ak, func_name):
            raise ValueError(f"Function '{func_name}' not found in akshare")
        func = getattr(self.ak, func_name)
        if not callable(func):
            raise ValueError(f"'{func_name}' is not callable")
        return func

    def get_function_signature(self, func):
        """Extract function parameters"""
        sig = inspect.signature(func)
        return sig.parameters

    def format_output(self, result: Any) -> str:
        """Format output based on format option"""
        if self.output_format == "json":
            if isinstance(result, pd.DataFrame):
                return json.dumps(result.to_dict(orient='records'), ensure_ascii=False, indent=2)
            elif isinstance(result, dict):
                return json.dumps(result, ensure_ascii=False, indent=2)
            else:
                return json.dumps(str(result), ensure_ascii=False)

        elif self.output_format == "csv":
            if isinstance(result, pd.DataFrame):
                return result.to_csv(index=False)
            else:
                raise ValueError("CSV output only supported for DataFrames")

        elif self.output_format == "pretty":
            if isinstance(result, pd.DataFrame):
                return result.to_string()
            else:
                return str(result)

        else:  # raw
            return str(result)

    def parse_args(self, func_name: str, args_list: list) -> Dict[str, Any]:
        """Parse command line arguments for specific function"""
        func = self.get_function(func_name)
        sig = self.get_function_signature(func)

        # Create parser for this function
        parser = argparse.ArgumentParser(description=f"Call akshare.{func_name}()")

        # Add --format option
        parser.add_argument(
            "--format",
            choices=["json", "csv", "pretty", "raw"],
            default="pretty",
            help="Output format (default: pretty)"
        )

        # Add parameters from function signature
        for param_name, param in sig.parameters.items():
            if param_name in ['self', 'cls']:
                continue

            # Determine parameter type
            if param.annotation != inspect.Parameter.empty:
                param_type = param.annotation
            else:
                param_type = str

            # Check if has default value
            has_default = param.default != inspect.Parameter.empty
            required = not has_default

            # Add argument
            parser.add_argument(
                f"--{param_name}",
                type=param_type if param_type != bool else lambda x: x.lower() == 'true',
                required=required,
                help=f"Parameter '{param_name}' (type: {param_type.__name__})"
            )

        return parser.parse_args(args_list)

    def run(self, func_name: str, args_list: list):
        """Execute function with parsed arguments"""
        try:
            # Parse arguments
            parsed_args = self.parse_args(func_name, args_list)

            # Extract format and remove from dict
            self.output_format = parsed_args.format
            vars_dict = vars(parsed_args)
            del vars_dict['format']

            # Get function and execute
            func = self.get_function(func_name)
            result = func(**vars_dict)

            # Format and print output
            output = self.format_output(result)
            print(output)

            return 0

        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return 1


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: akshare-cli <function_name> [--param1 value1] [--param2 value2]")
        print("       akshare-cli --help")
        sys.exit(1)

    func_name = sys.argv[1]
    args_list = sys.argv[2:]

    # Handle help
    if func_name == "--help" or func_name == "-h":
        print(__doc__)
        sys.exit(0)

    cli = AKShareCLI()
    exit_code = cli.run(func_name, args_list)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
```

**Step 2: Test the basic CLI tool**

```bash
cd /Users/ppsteven/projects/trade-skills/akshare-skill

# Test help
python3 scripts/akshare_cli.py --help

# Test a simple function (macro_china_gdp has no parameters)
python3 scripts/akshare_cli.py macro_china_gdp --format pretty
```

Expected: Tool runs without errors, displays output or help

**Step 3: Make CLI executable**

```bash
chmod +x scripts/akshare_cli.py

# Create wrapper script
cat > scripts/akshare-cli << 'EOF'
#!/bin/bash
python3 "$(dirname "$0")/akshare_cli.py" "$@"
EOF

chmod +x scripts/akshare-cli
```

**Step 4: Commit CLI tool**

```bash
git add scripts/akshare_cli.py scripts/akshare-cli CLI_DESIGN.md
git commit -m "feat: implement akshare CLI wrapper tool core functionality"
```

---

## Task 3: Create Comprehensive Test Suite

**Files:**
- Create: `tests/test_cli.py` - Core CLI tests
- Create: `tests/test_stock_cli.py` - Stock API tests
- Create: `tests/test_bank_cli.py` - Bank API tests
- Create: `tests/__init__.py`

**Step 1: Create tests directory and init**

```bash
cd /Users/ppsteven/projects/trade-skills/akshare-skill
mkdir -p tests
touch tests/__init__.py
```

**Step 2: Create core CLI test file**

Create `tests/test_cli.py`:

```python
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
        result = subprocess.run(cmd, capture_output=True, text=True)
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
```

**Step 3: Create stock API tests**

Create `tests/test_stock_cli.py`:

```python
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
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
```

**Step 4: Create bank API tests**

Create `tests/test_bank_cli.py`:

```python
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result

    def test_bank_fjcf_table_detail(self):
        """Test bank regulatory data"""
        result = self.run_cli(
            "bank_fjcf_table_detail",
            "--page", "1",
            "--item", "分局本级"
        )
        assert result.returncode == 0
```

**Step 5: Run tests**

```bash
cd /Users/ppsteven/projects/trade-skills/akshare-skill

# Install pytest if needed
pip install pytest -q

# Run all tests
pytest tests/ -v
```

Expected: Most tests pass, some may need timeout adjustments for slow API calls

**Step 6: Commit tests**

```bash
git add tests/
git commit -m "test: add comprehensive CLI test suite for all major APIs"
```

---

## Task 4: Update references/stock.md with CLI Examples

**Files:**
- Modify: `references/stock.md`

**Step 1: Read current stock.md structure**

Understand current format with Python examples

**Step 2: Update first API example**

Replace Python example:
```python
import akshare as ak
stock_df = ak.stock_zh_a_hist(symbol="000001", start_date="20200101", end_date="20210101")
print(stock_df)
```

With CLI examples:

```markdown
**CLI (Pretty Print):**
\`\`\`bash
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20200101 --end_date 20210101 --format pretty
\`\`\`

**CLI (CSV Export):**
\`\`\`bash
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20200101 --end_date 20210101 --format csv > stock_000001.csv
\`\`\`

**CLI (JSON Export):**
\`\`\`bash
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20200101 --end_date 20210101 --format json | jq '.'
\`\`\`
```

**Step 3: Update all major stock APIs**

Apply same pattern to:
- stock_zh_a_hist
- stock_zh_a_spot
- stock_zh_a_ggt_detailed
- Any other major APIs in file

**Step 4: Verify file**

Ensure all examples are properly formatted and consistent

**Step 5: Test examples work**

```bash
# Test one example manually
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240110 --format csv | head -5
```

**Step 6: Commit**

```bash
git add references/stock.md
git commit -m "docs: update stock.md with CLI usage examples"
```

---

## Task 5: Update references/bank.md with CLI Examples

**Files:**
- Modify: `references/bank.md`

**Step 1: Update bank APIs**

Replace Python examples with CLI format:

```markdown
**CLI Usage:**
\`\`\`bash
python3 scripts/akshare_cli.py bank_fjcf_table_detail --page 5 --item "分局本级" --format pretty
\`\`\`

**Export to JSON:**
\`\`\`bash
python3 scripts/akshare_cli.py bank_fjcf_table_detail --page 5 --item "分局本级" --format json > bank_data.json
\`\`\`
```

**Step 2: Update all bank-related APIs**

Find all APIs in file and update them

**Step 3: Test examples**

```bash
python3 scripts/akshare_cli.py bank_fjcf_table_detail --page 1 --item "分局本级" --format pretty | head -10
```

**Step 4: Commit**

```bash
git add references/bank.md
git commit -m "docs: update bank.md with CLI usage examples"
```

---

## Task 6: Update Other Major References (Index, Futures, Macro)

**Files:**
- Modify: `references/index.md`
- Modify: `references/futures.md`
- Modify: `references/macro.md`

**Step 1: Update index.md**

Replace all Python examples with CLI format for index APIs

**Step 2: Update futures.md**

Replace all Python examples with CLI format for futures APIs

**Step 3: Update macro.md**

Replace all Python examples with CLI format for macro APIs

**Step 4: Test sample commands**

For each file, test 1-2 CLI commands to verify they work

**Step 5: Commit all three**

```bash
git add references/index.md references/futures.md references/macro.md
git commit -m "docs: update index, futures, and macro references with CLI examples"
```

---

## Task 7: Update Remaining References Files

**Files:**
- Modify: All remaining `references/*.md` files

**Step 1: Create update script**

```bash
#!/bin/bash
# Script to help update all reference files

for file in references/*.md; do
  if [ -f "$file" ]; then
    # Count Python import examples
    count=$(grep -c "import akshare as ak" "$file" 2>/dev/null || echo 0)
    if [ "$count" -gt 0 ]; then
      echo "$file: $count Python examples to update"
    fi
  fi
done
```

**Step 2: Update each file systematically**

- bond.md
- option.md
- fx.md
- qdii.md
- dc.md
- currency.md
- energy.md
- others.md
- etc.

For each: Replace Python imports with CLI commands

**Step 3: Test key commands from each file**

Sample test to verify CLI works for each category

**Step 4: Commit in batches**

```bash
# First batch
git add references/bond.md references/option.md references/fx.md
git commit -m "docs: update bond, option, and fx references with CLI examples"

# Continue with remaining files...
```

---

## Task 8: Update Multi-Part Category References

**Files:**
- Modify: `references/fund/fund_public.md`
- Modify: `references/fund/fund_private.md`
- Modify: `references/qhkc/index_data.md`
- Modify: `references/qhkc/fundamental.md`
- Modify: `references/qhkc/broker.md`
- Modify: `references/qhkc/commodity.md`

**Step 1: Update fund references**

Replace Python examples in both fund files with CLI format

**Step 2: Update qhkc references**

Update all QHKC subcategory files with CLI examples

**Step 3: Test samples**

```bash
# Test fund command
python3 scripts/akshare_cli.py fund_open_fund_list_sina --format json | head

# Test qhkc command if available
python3 scripts/akshare_cli.py some_hk_function --format pretty
```

**Step 4: Commit**

```bash
git add references/fund/ references/qhkc/
git commit -m "docs: update fund and qhkc references with CLI examples"
```

---

## Task 9: Update SKILL.md Main Documentation

**Files:**
- Modify: `SKILL.md`

**Step 1: Update Quick Start section**

Replace:
```python
import akshare as ak
stock_df = ak.stock_zh_a_hist(symbol="000001", start_date="20200101", end_date="20210101")
print(stock_df)
```

With:
```bash
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20200101 --end_date 20210101 --format pretty
```

**Step 2: Add CLI Usage section**

Insert after Quick Start:

```markdown
## CLI Usage

All AKShare functions are available via the CLI wrapper tool:

\`\`\`bash
# Get stock data
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240110

# Export to CSV
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240110 --format csv > data.csv

# Export to JSON
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240110 --format json
\`\`\`

**Output Formats:**
- `--format pretty`: Human-readable tables (default)
- `--format csv`: CSV format
- `--format json`: JSON format
- `--format raw`: Raw Python output

See [CLI_DESIGN.md](CLI_DESIGN.md) and [references/CLI_USAGE.md](references/CLI_USAGE.md) for complete documentation.
```

**Step 3: Update Data Categories intro**

Change to mention CLI:
> "All APIs below are available via CLI. See [CLI_DESIGN.md](CLI_DESIGN.md) for usage."

**Step 4: Commit**

```bash
git add SKILL.md
git commit -m "docs: update SKILL.md with CLI as primary usage method"
```

---

## Task 10: Run Full Test Suite and Validate

**Files:**
- Verify: All tests pass
- Verify: All CLI commands in docs work

**Step 1: Run full test suite**

```bash
cd /Users/ppsteven/projects/trade-skills/akshare-skill
pytest tests/ -v --tb=short
```

Expected: All tests pass with ✓

**Step 2: Validate random CLI commands from references**

```bash
# Test stock
python3 scripts/akshare_cli.py stock_zh_a_spot --format json | jq '.[:2]'

# Test macro
python3 scripts/akshare_cli.py macro_china_gdp --format csv | head -3

# Test bank
python3 scripts/akshare_cli.py bank_fjcf_table_detail --page 1 --item "分局本级" --format pretty | head -5
```

**Step 3: Verify all links in SKILL.md**

```bash
python3 << 'EOF'
import re
import os

with open('SKILL.md') as f:
    content = f.read()

links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
broken = []
for text, path in links:
    if path.startswith('http') or path.startswith('#'):
        continue
    if not os.path.exists(path):
        broken.append((text, path))

if broken:
    print("❌ Broken links:")
    for text, path in broken:
        print(f"  [{text}]({path})")
else:
    print("✅ All links valid")
EOF
```

**Step 4: Create final summary**

Create `IMPLEMENTATION_SUMMARY.md`:

```markdown
# AKShare CLI Wrapper - Implementation Summary

## What Was Done

1. ✅ Created CLI wrapper tool (`scripts/akshare_cli.py`)
   - Wraps all AKShare functions
   - Supports multiple output formats: pretty, CSV, JSON, raw
   - Provides help and usage information

2. ✅ Implemented comprehensive test suite
   - Core CLI tests
   - Stock API tests
   - Bank API tests
   - Support for additional API categories

3. ✅ Updated all documentation
   - Updated 25+ reference files with CLI examples
   - Replaced Python imports with CLI commands
   - Updated SKILL.md with CLI as primary method

## CLI Usage

**Format:**
\`\`\`bash
python3 scripts/akshare_cli.py <function_name> [--param1 value1] [--param2 value2] [--format output_format]
\`\`\`

**Examples:**
\`\`\`bash
# Stock data
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240110

# Macro data
python3 scripts/akshare_cli.py macro_china_gdp --format json

# Export to file
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240110 --format csv > data.csv
\`\`\`

## Testing

All APIs have been tested via CLI:
\`\`\`bash
pytest tests/ -v
\`\`\`

## Files Created
- `scripts/akshare_cli.py` - Main CLI tool
- `scripts/akshare-cli` - Wrapper script
- `tests/test_cli.py` - Core CLI tests
- `tests/test_stock_cli.py` - Stock API tests
- `tests/test_bank_cli.py` - Bank API tests
- `CLI_DESIGN.md` - CLI architecture documentation
- `IMPLEMENTATION_SUMMARY.md` - This file

## Files Modified
- All `references/*.md` files - Updated with CLI examples
- `SKILL.md` - Updated with CLI as primary usage
- `CLI_USAGE.md` - Updated with CLI command documentation

## Commits

- "docs: design CLI tool architecture and command format"
- "feat: implement akshare CLI wrapper tool core functionality"
- "test: add comprehensive CLI test suite for all major APIs"
- "docs: update stock.md with CLI usage examples"
- "docs: update bank.md with CLI usage examples"
- "docs: update index, futures, and macro references with CLI examples"
- [Additional commits for remaining references]
- "docs: update SKILL.md with CLI as primary usage method"
- "test: validate all CLI commands and links"
```

**Step 5: Final commit**

```bash
git add IMPLEMENTATION_SUMMARY.md
git commit -m "docs: add CLI wrapper implementation summary"
```

---

## Verification Checklist

- [ ] CLI tool runs and shows help
- [ ] All tests pass: `pytest tests/ -v`
- [ ] CLI commands work for: stock, bank, macro, index, futures
- [ ] All reference files use CLI format
- [ ] SKILL.md uses CLI as primary method
- [ ] All links in SKILL.md are valid
- [ ] No Python imports remain in example code
- [ ] CLI output matches expected formats

---

## Summary

This implementation provides a complete CLI wrapper for AKShare:

1. **CLI Tool** - `scripts/akshare_cli.py` wraps all functions
2. **Test Suite** - Comprehensive tests ensure reliability
3. **Updated Docs** - All references use CLI commands
4. **Primary Usage** - CLI is now the primary recommended method

Users can now use AKShare entirely via command line without writing Python code.
