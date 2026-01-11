# Options Trade Tracker (Python)

A Python-based CLI application for parsing brokerage trade data, tracking open options positions, realized P&L, investments, and exporting results to Excel.

## Features
- Parses Robinhood-style brokerage CSV trade history
- Tracks open vs. closed options positions (calls & puts)
- Calculates realized P&L for options trades
- Handles dividends, partial shares, and cash activity
- Menu-driven command-line interface (CLI)
- Unit-tested core parsing logic
- Exports structured results to Excel (.xlsx)

## Tech Stack
- Python
- pandas
- unittest
- Excel export (.xlsx)

## How It Works
1. Import brokerage trade history from a CSV file
2. Parse and categorize trades (options, investments, cash activity)
3. Calculate open positions and realized P&L
4. Export clean, structured data to Excel for analysis

## Status
Actively developed — features and refinements ongoing.

## Why This Project
Built to better understand options trading mechanics, trade lifecycles, and financial data parsing in Python.  
This project also demonstrates real-world data handling, CLI design, and modular Python development.
