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
        try:
            sig = inspect.signature(func)
            # Convert to dict to handle mappingproxy objects
            return dict(sig.parameters)
        except (ValueError, TypeError):
            # If signature fails, return empty dict
            return {}

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
        params_dict = self.get_function_signature(func)

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
        for param_name, param in params_dict.items():
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
