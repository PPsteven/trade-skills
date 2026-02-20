# AKShare CLI Tool Design

## Command Format

```bash
akshare-cli <function_name> [--param1 value1] [--param2 value2] [--format output_format]
```

## Usage Examples

```bash
# Get stock data (JSON output is default)
akshare-cli stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131

# Get macro data (JSON is default)
akshare-cli macro_china_gdp

# Get as CSV when needed for complex analysis
akshare-cli stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131 --format csv

# Get as pretty table for human reading
akshare-cli bank_fjcf_table_detail --page 5 --item "分局本级" --format pretty
```

## Output Formats

- **json**: JSON format (default)
- **pretty**: Human-readable table format
- **csv**: CSV format (use when complex analysis is needed)
- **raw**: Raw Python object representation

## Parameter Types

Automatically detected from function signature:
- `str`: String parameters
- `int`: Integer parameters
- `bool`: Boolean flags (--flag for True, --no-flag for False)
- `float`: Float parameters
- `datetime`/`date`: Date parameters
