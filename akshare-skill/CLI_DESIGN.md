# AKShare CLI Tool Design

## Command Format

```bash
akshare-cli <function_name> [--param1 value1] [--param2 value2] [--format output_format]
```

## Usage Examples

```bash
# Get stock data
akshare-cli stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240131 --format csv

# Get macro data
akshare-cli macro_china_gdp --format json

# Get bank penalties
akshare-cli bank_fjcf_table_detail --page 5 --item "分局本级" --format pretty
```

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
