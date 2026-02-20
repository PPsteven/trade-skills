# AKShare CLI 快速开始指南

## 安装

确保已安装 Python 3.6+ 和 akshare 库：

```bash
pip install akshare
```

## 基本命令格式

```bash
python3 scripts/akshare_cli.py <function_name> [--param1 value1] [--param2 value2] [--format output_format]
```

## 常用命令示例

### 1. 查看帮助
```bash
python3 scripts/akshare_cli.py --help
```

### 2. 宏观经济数据

**获取中国 GDP 数据（表格格式）**
```bash
python3 scripts/akshare_cli.py macro_china_gdp --format pretty
```

**导出为 JSON**
```bash
python3 scripts/akshare_cli.py macro_china_gdp --format json
```

**导出为 CSV**
```bash
python3 scripts/akshare_cli.py macro_china_gdp --format csv > gdp.csv
```

**获取 CPI 数据**
```bash
python3 scripts/akshare_cli.py macro_china_cpi_yearly --format pretty
```

### 3. 股票数据（如果 API 可用）

**获取 A 股历史数据**
```bash
python3 scripts/akshare_cli.py stock_zh_a_hist \
  --symbol 000001 \
  --start_date 20240101 \
  --end_date 20240131 \
  --format pretty
```

**导出为 CSV**
```bash
python3 scripts/akshare_cli.py stock_zh_a_hist \
  --symbol 000001 \
  --start_date 20240101 \
  --end_date 20240131 \
  --format csv > stock.csv
```

### 4. 指数数据

**获取指数历史数据**
```bash
python3 scripts/akshare_cli.py index_zh_a_hist \
  --symbol 000001 \
  --start_date 20240101 \
  --end_date 20240131 \
  --format pretty
```

### 5. 银行数据（如果 API 可用）

**获取银保监处罚信息**
```bash
python3 scripts/akshare_cli.py bank_fjcf_table_detail \
  --page 1 \
  --item "分局本级" \
  --format pretty
```

## 输出格式说明

| 格式 | 说明 | 用途 |
|------|------|------|
| `pretty` | 人类可读表格（默认） | 终端查看 |
| `csv` | 逗号分隔值 | Excel、数据库导入 |
| `json` | JSON 格式 | API、程序集成 |
| `raw` | 原始 Python 表示 | 调试 |

## 常见用法

### 批量下载数据
```bash
#!/bin/bash
for symbol in 000001 000002 000004; do
  python3 scripts/akshare_cli.py stock_zh_a_hist \
    --symbol $symbol \
    --start_date 20240101 \
    --end_date 20240131 \
    --format csv > stock_$symbol.csv
done
```

### 定时更新数据
```bash
# 每天 9:30 执行
*/30 9 * * * /path/to/akshare-cli.sh stock_zh_a_hist --symbol 000001 --start_date $(date +%Y%m%d) --end_date $(date +%Y%m%d) --format csv >> /path/to/today_data.csv
```

### 数据管道处理
```bash
# 获取数据并用 jq 处理
python3 scripts/akshare_cli.py macro_china_gdp --format json | jq '.[0:3]'

# 获取 CSV 数据并用 awk 处理
python3 scripts/akshare_cli.py macro_china_gdp --format csv | awk -F',' '{sum+=$2} END {print sum}'
```

## 错误处理

### 无效的函数名
```bash
$ python3 scripts/akshare_cli.py invalid_function
Error: Function 'invalid_function' not found in akshare
```

### 缺失必需参数
```bash
$ python3 scripts/akshare_cli.py stock_zh_a_hist
usage: ... [-h] [--format {json,csv,pretty,raw}] --symbol SYMBOL --start_date START_DATE --end_date END_DATE
... required: --symbol, --start_date, --end_date
```

## 支持的 API 函数

所有 AKShare 1076+ 个公开函数都支持。常见的包括：

- **股票数据**: stock_zh_a_hist, stock_zh_a_spot, stock_bk_list
- **指数数据**: index_zh_a_hist, index_zh_a_component_detailed
- **期货数据**: futures_inventory_em, futures_delivery_dce
- **宏观数据**: macro_china_gdp, macro_china_cpi_yearly, macro_china_trade_balance
- **债券数据**: bond_zh_*
- **期权数据**: option_*
- **外汇数据**: fx_*
- **QDII 数据**: qdii_*

查看 `references/` 目录中的文档了解详细参数说明。

## 文档

- **CLI_DESIGN.md** - CLI 工具架构设计
- **references/** - 按类别组织的 API 文档
  - stock.md - 股票数据 APIs
  - index.md - 指数数据 APIs
  - macro.md - 宏观数据 APIs
  - ... 等等
- **SKILL.md** - 完整的 AKShare 技能文档
- **IMPLEMENTATION_SUMMARY.md** - 实现细节总结

## 测试

运行测试套件验证安装：

```bash
pytest tests/ -v
```

## 故障排除

**问题**: "urllib3 NotOpenSSLWarning"
**解决**: 这是警告而非错误，不影响功能。使用 `-W ignore` 忽略：
```bash
python3 -W ignore scripts/akshare_cli.py macro_china_gdp --format pretty
```

**问题**: API 返回错误或空数据
**解决**: 这可能是上游 AKShare API 的问题。CLI 工具会正确报告错误。

## 更多帮助

查看具体函数的帮助：
```bash
python3 scripts/akshare_cli.py macro_china_gdp --help
```

浏览参考文档了解所有支持的 API 和参数。
